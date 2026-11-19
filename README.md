# AI-Based Skill Gap Analysis for Students

A beginner-friendly full-stack implementation based on the uploaded research paper.

## Technology
- Frontend: React + Vite + jsPDF
- Backend: Python + Flask REST API + ReportLab
- Database: SQLite
- NLP: spaCy PhraseMatcher
- Semantic matching: Sentence-BERT (`all-MiniLM-L6-v2`) with a safe exact-match fallback
- Resume parsing: PyPDF and python-docx
- Report export: ReportLab vector PDF generator with client-side jsPDF fallback

## Requirements
Install:
1. Python 3.10 or newer
2. Node.js LTS (includes npm)
3. Visual Studio Code

## Folder structure
- `backend/` Flask API, AI engine and SQLite database
- `frontend/` React website
- `backend/uploads/` temporary resume storage (files are deleted after parsing)

## Run on Windows (VS Code terminal)

### A. Start backend
Open the project folder in VS Code, then open Terminal > New Terminal.

```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "from database import init_db; init_db(); print('Database created')"
python app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

On first AI analysis, Sentence-BERT may download the free `all-MiniLM-L6-v2` model. This requires internet and disk space. If the model cannot load, the app uses exact skill matching so you can still test the project.

Keep this terminal running. Backend: `http://127.0.0.1:5000`
Health check: `http://127.0.0.1:5000/api/health`

### B. Start frontend
Open a SECOND VS Code terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite, usually `http://localhost:5173`.

## Run on macOS/Linux
Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "from database import init_db; init_db(); print('Database created')"
python app.py
```
Frontend in a second terminal:
```bash
cd frontend
npm install
npm run dev
```

## First-time usage
1. Open the website.
2. Register with your name, email and password (minimum 6 characters).
3. Sign in.
4. Select Analyze resume.
5. Upload a text-based PDF or DOCX resume (maximum 5 MB).
6. Choose Data Analyst, Python Developer or Frontend Developer.
7. Optionally enter academic marks.
8. Generate the report.
9. Click **Download PDF Report** (at the top header or bottom of the report) to download your full assessment report as a PDF.

## Important academic notes
- The paper defines the gap as `max(0, required_level - current_level)`.
- Weighted score is `gap * skill_weight`; higher scores are prioritized.
- Resume extraction identifies skill mentions, not verified proficiency. This starter implementation uses a conservative default current level of 40 when a skill is detected, and 0 when not detected. A future enhancement should add a student self-rating form for each skill.
- Similarity matching uses Sentence-BERT embeddings and cosine similarity. The fallback uses exact matching if the model is not available.
- The course catalogue contains example free learning links. Check each provider's current access terms.
- This is an academic prototype, not a production deployment. Before public deployment, add persistent token sessions, CSRF/rate limiting, stronger upload scanning, admin authorization, privacy controls and HTTPS.
- The starter frontend is English-only, as requested.

## Database tables
The six core tables from the paper are implemented:
`students`, `student_skills`, `skills`, `job_roles`, `role_skills`, `courses`.

## Troubleshooting
- `python` not found: reinstall Python and enable "Add Python to PATH"; on Windows try `py`.
- `npm` not found: install Node.js LTS and restart VS Code.
- Frontend cannot connect: ensure Flask is running on port 5000.
- PDF has no extracted text: it may be a scanned image; OCR is not included in this paper-aligned first version.
- Model download fails: retry with internet access; exact matching fallback remains available.
