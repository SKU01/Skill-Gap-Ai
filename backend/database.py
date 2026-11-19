import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).with_name("skill_gap.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            branch TEXT DEFAULT '',
            year TEXT DEFAULT '',
            target_role_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL UNIQUE,
            category TEXT DEFAULT 'Technical'
        );
        CREATE TABLE IF NOT EXISTS student_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            level INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY(skill_id) REFERENCES skills(skill_id),
            UNIQUE(student_id, skill_id)
        );
        CREATE TABLE IF NOT EXISTS job_roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS role_skills (
            role_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            required_level INTEGER NOT NULL DEFAULT 70,
            weight REAL NOT NULL DEFAULT 1,
            PRIMARY KEY(role_id, skill_id),
            FOREIGN KEY(role_id) REFERENCES job_roles(role_id) ON DELETE CASCADE,
            FOREIGN KEY(skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            skill_id INTEGER NOT NULL,
            provider TEXT DEFAULT '',
            level TEXT DEFAULT 'Beginner',
            url TEXT DEFAULT '',
            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
        );
        """)

        # Seed skills and job roles based on the paper's sample Data Analyst role.
        skill_data = [
            ("Python","Programming"),("SQL","Database"),("Machine Learning","AI/ML"),
            ("Cloud","Cloud Computing"),("Communication","Soft Skills"),
            ("Excel","Analytics"),("Statistics","Analytics"),("Data Visualization","Analytics"),
            ("Power BI","Analytics"),("Git","Tools"),("HTML","Web"),("JavaScript","Web")
        ]
        for name, cat in skill_data:
            db.execute("INSERT OR IGNORE INTO skills(skill_name,category) VALUES (?,?)",(name,cat))

        roles = {
            "Data Analyst": ("Analyze data and communicate business insights.",
                {"Python":(80,1.0),"SQL":(75,1.0),"Machine Learning":(70,0.8),
                 "Cloud":(60,0.7),"Communication":(60,0.7),"Excel":(80,0.9),
                 "Statistics":(75,0.9),"Data Visualization":(75,0.9),"Power BI":(70,0.8)}),
            "Python Developer": ("Build applications and services using Python.",
                {"Python":(85,1.0),"SQL":(65,0.7),"Git":(70,0.7),"HTML":(50,0.4)}),
            "Frontend Developer": ("Build responsive web interfaces.",
                {"HTML":(85,1.0),"CSS":(80,1.0),"JavaScript":(85,1.0),"Git":(65,0.6),"Communication":(60,0.5)})
        }
        for role, (desc, reqs) in roles.items():
            db.execute("INSERT OR IGNORE INTO job_roles(role_name,description) VALUES (?,?)",(role,desc))
            role_id = db.execute("SELECT role_id FROM job_roles WHERE role_name=?",(role,)).fetchone()["role_id"]
            for skill, (level, weight) in reqs.items():
                db.execute("INSERT OR IGNORE INTO skills(skill_name,category) VALUES (?,?)",(skill,"Technical"))
                skill_id = db.execute("SELECT skill_id FROM skills WHERE skill_name=?",(skill,)).fetchone()["skill_id"]
                db.execute("""INSERT OR REPLACE INTO role_skills(role_id,skill_id,required_level,weight)
                              VALUES (?,?,?,?)""",(role_id,skill_id,level,weight))

        course_data = [
            ("Python for Everybody","Python","Coursera","Beginner","https://www.coursera.org/specializations/python"),
            ("SQL Tutorial","SQL","Khan Academy","Beginner","https://www.khanacademy.org/computing"),
            ("Intro to Machine Learning","Machine Learning","Kaggle","Beginner","https://www.kaggle.com/learn/intro-to-machine-learning"),
            ("Cloud Computing Basics","Cloud","AWS Skill Builder","Beginner","https://skillbuilder.aws/"),
            ("Communication Skills","Communication","OpenLearn","Beginner","https://www.open.edu/openlearn/"),
            ("Excel Skills for Business","Excel","Microsoft Learn","Beginner","https://learn.microsoft.com/training/"),
            ("Intro to Statistics","Statistics","Khan Academy","Beginner","https://www.khanacademy.org/math/statistics-probability"),
            ("Data Visualization","Data Visualization","Tableau","Beginner","https://www.tableau.com/learn/training"),
            ("Power BI Learning","Power BI","Microsoft Learn","Beginner","https://learn.microsoft.com/power-bi/"),
            ("Git Handbook","Git","GitHub","Beginner","https://docs.github.com/en/get-started"),
            ("HTML Learning Path","HTML","MDN","Beginner","https://developer.mozilla.org/en-US/docs/Learn/HTML"),
            ("JavaScript Guide","JavaScript","MDN","Beginner","https://developer.mozilla.org/en-US/docs/Web/JavaScript")
        ]
        for title, skill, provider, level, url in course_data:
            sid = db.execute("SELECT skill_id FROM skills WHERE skill_name=?",(skill,)).fetchone()["skill_id"]
            db.execute("INSERT OR IGNORE INTO courses(title,skill_id,provider,level,url) VALUES (?,?,?,?,?)",
                       (title,sid,provider,level,url))
        db.commit()
