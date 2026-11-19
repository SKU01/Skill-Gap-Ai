import os, json, secrets
from io import BytesIO
from functools import wraps
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from docx import Document
from database import init_db, get_db
from ai_engine import extract_skills, semantic_match
from pdf_generator import create_report_pdf

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
UPLOAD_DIR = Path(__file__).with_name("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
TOKENS = {}

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization","").replace("Bearer ","")
        if token not in TOKENS:
            return jsonify({"error":"Please log in again."}), 401
        request.student_id = TOKENS[token]
        return fn(*args, **kwargs)
    return wrapper

def read_resume(path, ext):
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if ext == ".docx":
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Only PDF and DOCX files are supported.")

@app.get("/api/health")
def health():
    return jsonify({"status":"ok","message":"Skill Gap Analysis API is running"})

@app.post("/api/register")
def register():
    data = request.get_json() or {}
    name, email, password = data.get("name","").strip(), data.get("email","").strip().lower(), data.get("password","")
    if not name or not email or len(password) < 6:
        return jsonify({"error":"Enter your name, valid email and a password of at least 6 characters."}), 400
    try:
        with get_db() as db:
            db.execute("INSERT INTO students(name,email,password_hash,branch,year) VALUES (?,?,?,?,?)",
                       (name,email,generate_password_hash(password),data.get("branch",""),data.get("year","")))
            db.commit()
        return jsonify({"message":"Account created. You can now log in."}), 201
    except Exception:
        return jsonify({"error":"This email may already be registered."}), 409

@app.post("/api/login")
def login():
    data = request.get_json() or {}
    with get_db() as db:
        student = db.execute("SELECT * FROM students WHERE email=?",(data.get("email","").lower(),)).fetchone()
    if not student or not check_password_hash(student["password_hash"],data.get("password","")):
        return jsonify({"error":"Incorrect email or password."}), 401
    token = secrets.token_urlsafe(32)
    TOKENS[token] = student["student_id"]
    return jsonify({"token":token,"student":{"id":student["student_id"],"name":student["name"],"email":student["email"]}})

# Ensure database schema and seed data are up to date
init_db()

@app.get("/api/roles")
def roles():
    with get_db() as db:
        rows = db.execute("SELECT role_id,role_name,description,display_order FROM job_roles ORDER BY display_order ASC, role_id ASC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.get("/api/me")
@auth_required
def me():
    with get_db() as db:
        s = db.execute("SELECT student_id,name,email,branch,year FROM students WHERE student_id=?",
                       (request.student_id,)).fetchone()
    return jsonify(dict(s))

@app.post("/api/analyze")
@auth_required
def analyze():
    if "resume" not in request.files:
        return jsonify({"error":"Choose a PDF or DOCX resume."}), 400
    file = request.files["resume"]
    filename = secure_filename(file.filename or "")
    ext = Path(filename).suffix.lower()
    if ext not in [".pdf",".docx"]:
        return jsonify({"error":"Only PDF and DOCX files are supported."}), 400
    role_id = request.form.get("role_id")
    if not role_id:
        return jsonify({"error":"Select a target job role."}), 400
    temp_path = UPLOAD_DIR / f"{request.student_id}_{secrets.token_hex(4)}{ext}"
    file.save(temp_path)
    try:
        text = read_resume(temp_path,ext)
    except Exception as e:
        temp_path.unlink(missing_ok=True)
        return jsonify({"error":f"Could not read resume: {e}"}), 400
    finally:
        temp_path.unlink(missing_ok=True)

    extracted = extract_skills(text)
    self_assessment = json.loads(request.form.get("self_assessment","{}"))
    marks = request.form.get("marks","")
    with get_db() as db:
        role = db.execute("SELECT * FROM job_roles WHERE role_id=?",(role_id,)).fetchone()
        if not role:
            return jsonify({"error":"Selected job role was not found."}), 404
        required_rows = db.execute("""
            SELECT s.skill_id,s.skill_name,s.category,rs.required_level,rs.weight
            FROM role_skills rs JOIN skills s ON s.skill_id=rs.skill_id
            WHERE rs.role_id=?""",(role_id,)).fetchall()
        required_names = [r["skill_name"] for r in required_rows]
        similarities = semantic_match(extracted,required_names)
        report = []
        for r in required_rows:
            name = r["skill_name"]
            sim = similarities.get(name,0.0)
            # Resume presence is a signal, not proof of proficiency. Self-rating can refine it.
            resume_level = 40 if sim >= 0.55 else 0
            current = int(self_assessment.get(name,resume_level))
            current = max(0,min(100,current))
            gap = max(0,int(r["required_level"])-current)
            score = round(gap*float(r["weight"]),2)
            report.append({"skill":name,"category":r["category"],"current":current,
                           "required":r["required_level"],"gap":gap,"weight":r["weight"],
                           "score":score,"similarity":round(sim,3)})
            skill_id = r["skill_id"]
            db.execute("""INSERT INTO student_skills(student_id,skill_id,level) VALUES (?,?,?)
                          ON CONFLICT(student_id,skill_id) DO UPDATE SET level=excluded.level""",
                       (request.student_id,skill_id,current))
        db.execute("UPDATE students SET target_role_id=? WHERE student_id=?",(role_id,request.student_id))
        db.commit()
    report.sort(key=lambda x:x["score"],reverse=True)
    top_skill_ids = []
    with get_db() as db:
        for item in report:
            if item["gap"] > 0:
                row = db.execute("SELECT skill_id FROM skills WHERE skill_name=?",(item["skill"],)).fetchone()
                if row: top_skill_ids.append(row["skill_id"])
        courses = []
        seen_titles = set()
        for sid in top_skill_ids:
            c = db.execute("SELECT title,provider,level,url FROM courses WHERE skill_id=?",(sid,)).fetchall()
            for x in c:
                if x["title"] not in seen_titles:
                    seen_titles.add(x["title"])
                    courses.append(dict(x))
    return jsonify({"role":role["role_name"],"extracted_skills":extracted,
                    "marks":marks,"report":report,"recommendations":courses[:8],
                    "note":"Resume detection indicates skill presence only. Review and adjust self-ratings for a more accurate proficiency estimate."})

@app.route("/api/report/pdf", methods=["GET", "POST"])
@auth_required
def download_report_pdf():
    with get_db() as db:
        student = db.execute("SELECT student_id, name, email, branch, year, target_role_id FROM students WHERE student_id=?",
                             (request.student_id,)).fetchone()
    if not student:
        return jsonify({"error": "Student profile not found."}), 404

    student_dict = dict(student)
    report_data = None

    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        report_data = data.get("report") or data

    if not report_data or not isinstance(report_data, dict) or not report_data.get("report"):
        target_role_id = student["target_role_id"]
        if not target_role_id:
            return jsonify({"error": "No previous analysis found. Please run an analysis first."}), 400

        with get_db() as db:
            role = db.execute("SELECT * FROM job_roles WHERE role_id=?", (target_role_id,)).fetchone()
            if not role:
                return jsonify({"error": "Job role not found."}), 404

            skills_rows = db.execute("""
                SELECT s.skill_id, s.skill_name, s.category, rs.required_level, rs.weight,
                       COALESCE(ss.level, 0) as current_level
                FROM role_skills rs
                JOIN skills s ON s.skill_id = rs.skill_id
                LEFT JOIN student_skills ss ON ss.skill_id = rs.skill_id AND ss.student_id = ?
                WHERE rs.role_id = ?
            """, (request.student_id, target_role_id)).fetchall()

            report = []
            top_skill_ids = []
            for r in skills_rows:
                current = int(r["current_level"])
                req = int(r["required_level"])
                gap = max(0, req - current)
                score = round(gap * float(r["weight"]), 2)
                report.append({
                    "skill": r["skill_name"],
                    "category": r["category"],
                    "current": current,
                    "required": req,
                    "gap": gap,
                    "weight": r["weight"],
                    "score": score
                })
                if gap > 0:
                    top_skill_ids.append(r["skill_id"])

            report.sort(key=lambda x: x["score"], reverse=True)
            courses = []
            seen_titles = set()
            for sid in top_skill_ids[:8]:
                c = db.execute("SELECT title, provider, level, url FROM courses WHERE skill_id=?", (sid,)).fetchall()
                for x in c:
                    if x["title"] not in seen_titles:
                        seen_titles.add(x["title"])
                        courses.append(dict(x))

            report_data = {
                "role": role["role_name"],
                "marks": "",
                "extracted_skills": [],
                "report": report,
                "recommendations": courses[:8],
                "note": "Resume detection indicates skill presence only. Review and adjust self-ratings for a more accurate proficiency estimate."
            }

    try:
        pdf_bytes = create_report_pdf(student_dict, report_data)
        role_slug = "".join(c if c.isalnum() else "_" for c in report_data.get("role", "Career")).strip("_")
        filename = f"SkillGapReport_{role_slug}.pdf"
        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500

if __name__ == "__main__":
    init_db()
    print("Database ready. Open http://127.0.0.1:5000/api/health")
    app.run(debug=True,port=5000)
