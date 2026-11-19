import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("skill_gap.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

ROLES_DATA = [
    {
        "order": 1,
        "name": "Data Analyst",
        "description": "Analyze complex datasets and communicate actionable business insights.",
        "skills": {
            "SQL": (80, 1.0),
            "Python": (75, 0.9),
            "Excel": (85, 0.9),
            "Power BI": (75, 0.8),
            "Tableau": (70, 0.8),
            "Statistics": (75, 0.9),
            "Data Visualization": (80, 0.9),
            "Communication": (70, 0.7)
        }
    },
    {
        "order": 2,
        "name": "Data Scientist",
        "description": "Extract actionable insights, build predictive models, and deploy machine learning solutions.",
        "skills": {
            "Python": (85, 1.0),
            "Machine Learning": (85, 1.0),
            "Statistics": (80, 0.9),
            "Deep Learning": (75, 0.8),
            "SQL": (75, 0.8),
            "Data Analysis": (80, 0.8),
            "Data Visualization": (70, 0.7),
            "Pandas": (80, 0.8)
        }
    },
    {
        "order": 3,
        "name": "Python Developer",
        "description": "Build scalable backends, web services, automation, and APIs using Python.",
        "skills": {
            "Python": (90, 1.0),
            "Django": (75, 0.8),
            "Flask": (75, 0.8),
            "SQL": (70, 0.8),
            "REST APIs": (80, 0.9),
            "Git": (75, 0.7),
            "Data Structures": (80, 0.9),
            "Docker": (65, 0.6)
        }
    },
    {
        "order": 4,
        "name": "Java Developer",
        "description": "Develop enterprise-grade backend applications and microservices using Java and Spring.",
        "skills": {
            "Java": (90, 1.0),
            "Spring Boot": (85, 1.0),
            "Hibernate": (75, 0.8),
            "SQL": (75, 0.8),
            "REST APIs": (80, 0.9),
            "Microservices": (75, 0.8),
            "Git": (75, 0.7),
            "Object-Oriented Programming": (85, 0.9)
        }
    },
    {
        "order": 5,
        "name": "Full Stack Developer",
        "description": "Build complete end-to-end web applications across client-side and server-side architectures.",
        "skills": {
            "JavaScript": (85, 1.0),
            "React": (80, 0.9),
            "Node.js": (80, 0.9),
            "HTML": (85, 0.7),
            "CSS": (80, 0.7),
            "SQL": (75, 0.8),
            "MongoDB": (70, 0.7),
            "REST APIs": (80, 0.9),
            "Git": (75, 0.8)
        }
    },
    {
        "order": 6,
        "name": "Frontend Developer",
        "description": "Build intuitive, responsive, and high-performance user interfaces for the web.",
        "skills": {
            "HTML": (90, 0.9),
            "CSS": (85, 0.9),
            "JavaScript": (90, 1.0),
            "React": (85, 1.0),
            "TypeScript": (75, 0.8),
            "Responsive Design": (80, 0.8),
            "Git": (70, 0.7),
            "UI/UX Design": (65, 0.6)
        }
    },
    {
        "order": 7,
        "name": "Backend Developer",
        "description": "Design and implement core server-side logic, database architectures, and secure APIs.",
        "skills": {
            "Python": (80, 0.9),
            "Node.js": (80, 0.9),
            "SQL": (85, 1.0),
            "REST APIs": (85, 1.0),
            "Database Management": (80, 0.8),
            "Docker": (70, 0.7),
            "Git": (75, 0.7),
            "Microservices": (70, 0.7)
        }
    },
    {
        "order": 8,
        "name": "Web Developer",
        "description": "Create, maintain, and optimize responsive websites and web applications.",
        "skills": {
            "HTML": (90, 1.0),
            "CSS": (85, 1.0),
            "JavaScript": (85, 1.0),
            "Responsive Design": (80, 0.8),
            "PHP": (70, 0.7),
            "MySQL": (75, 0.8),
            "Git": (70, 0.7),
            "Web Security": (65, 0.6)
        }
    },
    {
        "order": 9,
        "name": "Machine Learning Engineer",
        "description": "Design, build, train, and deploy production-grade machine learning models and pipelines.",
        "skills": {
            "Python": (90, 1.0),
            "Machine Learning": (90, 1.0),
            "Deep Learning": (80, 0.9),
            "Scikit-learn": (85, 0.9),
            "PyTorch": (80, 0.9),
            "TensorFlow": (75, 0.8),
            "MLOps": (70, 0.8),
            "Statistics": (80, 0.8)
        }
    },
    {
        "order": 10,
        "name": "AI Engineer",
        "description": "Architect and integrate state-of-the-art AI systems, LLMs, and intelligent applications.",
        "skills": {
            "Python": (90, 1.0),
            "Artificial Intelligence": (90, 1.0),
            "NLP": (85, 0.9),
            "Deep Learning": (85, 0.9),
            "Generative AI": (85, 1.0),
            "PyTorch": (80, 0.8),
            "Cloud": (75, 0.7),
            "Computer Vision": (70, 0.7)
        }
    },
    {
        "order": 11,
        "name": "Software Engineer",
        "description": "Design, develop, and maintain robust software systems using core computer science principles.",
        "skills": {
            "Data Structures": (85, 1.0),
            "Algorithms": (85, 1.0),
            "Object-Oriented Programming": (85, 0.9),
            "Java": (80, 0.8),
            "Python": (80, 0.8),
            "Git": (75, 0.7),
            "System Design": (75, 0.8),
            "SQL": (70, 0.7)
        }
    },
    {
        "order": 12,
        "name": "Cloud Engineer",
        "description": "Architect, deploy, and manage secure, scalable infrastructure on public cloud platforms.",
        "skills": {
            "Cloud": (90, 1.0),
            "AWS": (85, 1.0),
            "Linux": (80, 0.9),
            "Docker": (75, 0.8),
            "Kubernetes": (75, 0.8),
            "Terraform": (70, 0.7),
            "Networking": (75, 0.8),
            "DevOps": (70, 0.7)
        }
    },
    {
        "order": 13,
        "name": "DevOps Engineer",
        "description": "Streamline software delivery and operations through automated CI/CD and infrastructure as code.",
        "skills": {
            "Linux": (85, 0.9),
            "CI/CD": (85, 1.0),
            "Docker": (85, 1.0),
            "Kubernetes": (80, 0.9),
            "Jenkins": (75, 0.8),
            "Git": (80, 0.8),
            "Terraform": (75, 0.8),
            "Cloud": (80, 0.8),
            "Bash": (75, 0.7)
        }
    },
    {
        "order": 14,
        "name": "Cybersecurity Analyst",
        "description": "Protect systems, networks, and data from cyber threats, vulnerabilities, and security breaches.",
        "skills": {
            "Network Security": (85, 1.0),
            "Information Security": (85, 1.0),
            "Ethical Hacking": (75, 0.8),
            "Linux": (80, 0.8),
            "Wireshark": (75, 0.8),
            "Vulnerability Assessment": (80, 0.9),
            "Cryptography": (70, 0.7),
            "SIEM": (70, 0.7)
        }
    },
    {
        "order": 15,
        "name": "Database Administrator",
        "description": "Ensure performance, integrity, security, and high availability of organizational databases.",
        "skills": {
            "SQL": (95, 1.0),
            "MySQL": (85, 0.9),
            "PostgreSQL": (85, 0.9),
            "Database Administration": (90, 1.0),
            "Performance Tuning": (80, 0.9),
            "Backup & Recovery": (80, 0.8),
            "Data Modeling": (75, 0.8),
            "Linux": (70, 0.7)
        }
    },
    {
        "order": 16,
        "name": "Business Analyst",
        "description": "Bridge business needs and technology solutions by analyzing processes and specifying requirements.",
        "skills": {
            "Business Analysis": (90, 1.0),
            "Requirements Gathering": (85, 1.0),
            "Excel": (85, 0.9),
            "SQL": (70, 0.8),
            "Data Visualization": (75, 0.8),
            "Agile": (80, 0.8),
            "Communication": (90, 1.0),
            "JIRA": (75, 0.7)
        }
    },
    {
        "order": 17,
        "name": "UI/UX Designer",
        "description": "Craft engaging, accessible, and user-centered digital product experiences and interfaces.",
        "skills": {
            "UI/UX Design": (95, 1.0),
            "Figma": (90, 1.0),
            "Wireframing": (85, 0.9),
            "Prototyping": (85, 0.9),
            "User Research": (80, 0.8),
            "Design Systems": (80, 0.8),
            "HTML": (65, 0.6),
            "CSS": (65, 0.6)
        }
    },
    {
        "order": 18,
        "name": "Android Developer",
        "description": "Build responsive, feature-rich native Android mobile applications.",
        "skills": {
            "Kotlin": (85, 1.0),
            "Java": (80, 0.8),
            "Android Studio": (85, 0.9),
            "Android SDK": (85, 1.0),
            "REST APIs": (75, 0.8),
            "Git": (75, 0.7),
            "SQLite": (70, 0.7),
            "MVVM": (75, 0.8)
        }
    },
    {
        "order": 19,
        "name": "Software Tester / QA Engineer",
        "description": "Ensure software quality and reliability through comprehensive manual and automated testing.",
        "skills": {
            "Manual Testing": (85, 1.0),
            "Automation Testing": (85, 1.0),
            "Selenium": (80, 0.9),
            "Java": (75, 0.8),
            "Python": (75, 0.8),
            "API Testing": (80, 0.9),
            "JIRA": (80, 0.8),
            "SQL": (70, 0.7)
        }
    },
    {
        "order": 20,
        "name": "Network Engineer",
        "description": "Design, implement, and maintain resilient local and wide-area network infrastructures.",
        "skills": {
            "Networking": (90, 1.0),
            "TCP/IP": (85, 1.0),
            "Routing & Switching": (85, 0.9),
            "Cisco": (80, 0.9),
            "Firewalls": (80, 0.8),
            "Wireshark": (75, 0.8),
            "Linux": (75, 0.7),
            "Network Troubleshooting": (85, 0.9)
        }
    }
]

SKILL_CATEGORIES = {
    "SQL": "Database",
    "Python": "Programming",
    "Excel": "Analytics",
    "Power BI": "Analytics",
    "Tableau": "Analytics",
    "Statistics": "Analytics",
    "Data Visualization": "Analytics",
    "Communication": "Soft Skills",
    "Machine Learning": "AI/ML",
    "Deep Learning": "AI/ML",
    "Data Analysis": "Analytics",
    "Pandas": "Analytics",
    "Django": "Web Frameworks",
    "Flask": "Web Frameworks",
    "REST APIs": "Backend",
    "Git": "Tools",
    "Data Structures": "Computer Science",
    "Docker": "DevOps & Cloud",
    "Java": "Programming",
    "Spring Boot": "Backend Frameworks",
    "Hibernate": "Backend Frameworks",
    "Microservices": "Architecture",
    "Object-Oriented Programming": "Computer Science",
    "JavaScript": "Web & Programming",
    "React": "Frontend Frameworks",
    "Node.js": "Backend",
    "HTML": "Web",
    "CSS": "Web",
    "MongoDB": "Database",
    "TypeScript": "Programming",
    "Responsive Design": "Web",
    "UI/UX Design": "Design",
    "Database Management": "Database",
    "PHP": "Web Programming",
    "MySQL": "Database",
    "Web Security": "Security",
    "Scikit-learn": "AI/ML",
    "PyTorch": "AI/ML",
    "TensorFlow": "AI/ML",
    "MLOps": "AI/ML",
    "Artificial Intelligence": "AI/ML",
    "NLP": "AI/ML",
    "Generative AI": "AI/ML",
    "Cloud": "Cloud Computing",
    "Computer Vision": "AI/ML",
    "Algorithms": "Computer Science",
    "System Design": "Architecture",
    "AWS": "Cloud Computing",
    "Linux": "Operating Systems",
    "Kubernetes": "DevOps & Cloud",
    "Terraform": "DevOps & Cloud",
    "Networking": "Networking",
    "DevOps": "DevOps & Cloud",
    "CI/CD": "DevOps & Cloud",
    "Jenkins": "DevOps & Cloud",
    "Bash": "Tools",
    "Network Security": "Cybersecurity",
    "Information Security": "Cybersecurity",
    "Ethical Hacking": "Cybersecurity",
    "Wireshark": "Cybersecurity & Networking",
    "Vulnerability Assessment": "Cybersecurity",
    "Cryptography": "Cybersecurity",
    "SIEM": "Cybersecurity",
    "PostgreSQL": "Database",
    "Database Administration": "Database",
    "Performance Tuning": "Database",
    "Backup & Recovery": "Database",
    "Data Modeling": "Database",
    "Business Analysis": "Business & Management",
    "Requirements Gathering": "Business & Management",
    "Agile": "Methodology",
    "JIRA": "Tools",
    "Figma": "Design",
    "Wireframing": "Design",
    "Prototyping": "Design",
    "User Research": "Design",
    "Design Systems": "Design",
    "Kotlin": "Mobile Programming",
    "Android Studio": "Mobile Development",
    "Android SDK": "Mobile Development",
    "SQLite": "Database",
    "MVVM": "Architecture",
    "Manual Testing": "Testing & QA",
    "Automation Testing": "Testing & QA",
    "Selenium": "Testing & QA",
    "API Testing": "Testing & QA",
    "TCP/IP": "Networking",
    "Routing & Switching": "Networking",
    "Cisco": "Networking",
    "Firewalls": "Networking & Security",
    "Network Troubleshooting": "Networking"
}

COURSE_CATALOG = [
    ("Python for Everybody", "Python", "Coursera", "Beginner", "https://www.coursera.org/specializations/python"),
    ("SQL Tutorial & Practice", "SQL", "Khan Academy", "Beginner", "https://www.khanacademy.org/computing"),
    ("Intro to Machine Learning", "Machine Learning", "Kaggle", "Beginner", "https://www.kaggle.com/learn/intro-to-machine-learning"),
    ("Deep Learning Specialization", "Deep Learning", "Coursera", "Intermediate", "https://www.coursera.org/specializations/deep-learning"),
    ("AI for Everyone", "Artificial Intelligence", "Coursera / DeepLearning.AI", "Beginner", "https://www.coursera.org/learn/ai-for-everyone"),
    ("Natural Language Processing Specialization", "NLP", "Coursera", "Intermediate", "https://www.coursera.org/specializations/natural-language-processing"),
    ("Generative AI for Beginners", "Generative AI", "Microsoft Learn", "Beginner", "https://github.com/microsoft/generative-ai-for-beginners"),
    ("Machine Learning with Scikit-Learn", "Scikit-learn", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/news/machine-learning-with-scikit-learn/"),
    ("Deep Learning with PyTorch", "PyTorch", "PyTorch Tutorials", "Intermediate", "https://pytorch.org/tutorials/"),
    ("TensorFlow Developer Certificate Guide", "TensorFlow", "TensorFlow", "Intermediate", "https://www.tensorflow.org/learn"),
    ("Intro to Statistics", "Statistics", "Khan Academy", "Beginner", "https://www.khanacademy.org/math/statistics-probability"),
    ("Data Analysis with Python", "Data Analysis", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/learn/data-analysis-with-python/"),
    ("Data Analysis with Pandas", "Pandas", "Kaggle", "Beginner", "https://www.kaggle.com/learn/pandas"),
    ("Data Visualization with Tableau", "Data Visualization", "Tableau", "Beginner", "https://www.tableau.com/learn/training"),
    ("Power BI Learning Path", "Power BI", "Microsoft Learn", "Beginner", "https://learn.microsoft.com/power-bi/"),
    ("Tableau Fundamentals", "Tableau", "Tableau Public", "Beginner", "https://www.tableau.com/learn"),
    ("Excel Skills for Business", "Excel", "Microsoft Learn", "Beginner", "https://learn.microsoft.com/training/"),
    ("Effective Business Communication", "Communication", "OpenLearn", "Beginner", "https://www.open.edu/openlearn/"),
    ("Business Analysis Foundations", "Business Analysis", "LinkedIn Learning / Coursera", "Beginner", "https://www.coursera.org/learn/business-analysis-fundamentals"),
    ("Requirements Gathering & Engineering", "Requirements Gathering", "Coursera", "Beginner", "https://www.coursera.org/learn/requirements-engineering"),
    ("Agile with Atlassian Jira", "Agile", "Coursera / Atlassian", "Beginner", "https://www.coursera.org/learn/agile-atlassian-jira"),
    ("Jira Fundamentals", "JIRA", "Atlassian University", "Beginner", "https://university.atlassian.com/"),
    ("Java Programming Masterclass", "Java", "freeCodeCamp / Oracle", "Beginner", "https://dev.java/learn/"),
    ("Building Microservices with Spring Boot", "Spring Boot", "Spring.io", "Intermediate", "https://spring.io/guides"),
    ("Hibernate & JPA Guide", "Hibernate", "Baeldung", "Intermediate", "https://www.baeldung.com/learn-jpa-hibernate"),
    ("REST API Design & Development", "REST APIs", "MDN Web Docs", "Beginner", "https://developer.mozilla.org/en-US/docs/Glossary/REST"),
    ("Microservices Architecture Fundamentals", "Microservices", "Microsoft Learn", "Intermediate", "https://learn.microsoft.com/azure/architecture/guide/architecture-styles/microservices"),
    ("JavaScript Guide & Fundamentals", "JavaScript", "MDN Web Docs", "Beginner", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
    ("React Official Tutorial & Docs", "React", "React.dev", "Beginner", "https://react.dev/learn"),
    ("Node.js Complete Guide", "Node.js", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/news/learn-node-js/"),
    ("TypeScript for Beginners", "TypeScript", "TypeScriptLang", "Beginner", "https://www.typescriptlang.org/docs/handbook/intro.html"),
    ("HTML5 Learning Path", "HTML", "MDN Web Docs", "Beginner", "https://developer.mozilla.org/en-US/docs/Learn/HTML"),
    ("Modern CSS & Layouts", "CSS", "MDN Web Docs", "Beginner", "https://developer.mozilla.org/en-US/docs/Learn/CSS"),
    ("Responsive Web Design Certification", "Responsive Design", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/learn/2022/responsive-web-design/"),
    ("PHP Programming Tutorial", "PHP", "PHP.net", "Beginner", "https://www.php.net/manual/en/tutorial.php"),
    ("MySQL Tutorial for Beginners", "MySQL", "MySQL Official", "Beginner", "https://dev.mysql.com/doc/refman/8.0/en/tutorial.html"),
    ("PostgreSQL Tutorial", "PostgreSQL", "Postgresqltutorial", "Beginner", "https://www.postgresqltutorial.com/"),
    ("MongoDB Basics", "MongoDB", "MongoDB University", "Beginner", "https://learn.mongodb.com/"),
    ("Database Administrator Career Track", "Database Administration", "Microsoft Learn", "Intermediate", "https://learn.microsoft.com/training/paths/azure-database-admin/"),
    ("SQL Performance Tuning", "Performance Tuning", "Use The Index, Luke", "Intermediate", "https://use-the-index-luke.com/"),
    ("Data Modeling Foundations", "Data Modeling", "Coursera", "Beginner", "https://www.coursera.org/learn/database-design"),
    ("Database Backup and Recovery Basics", "Backup & Recovery", "Oracle Dev Gym", "Beginner", "https://devgym.oracle.com/"),
    ("Docker for Beginners", "Docker", "Docker Documentation", "Beginner", "https://docs.docker.com/get-started/"),
    ("Kubernetes Fundamentals", "Kubernetes", "Kubernetes.io", "Intermediate", "https://kubernetes.io/docs/tutorials/"),
    ("CI/CD with GitHub Actions", "CI/CD", "GitHub Skills", "Beginner", "https://skills.github.com/"),
    ("Jenkins User Guide & Tour", "Jenkins", "Jenkins.io", "Beginner", "https://www.jenkins.io/doc/pipeline/tour/getting-started/"),
    ("Terraform Associate Prep", "Terraform", "HashiCorp Learn", "Beginner", "https://developer.hashicorp.com/terraform/tutorials"),
    ("Introduction to Linux", "Linux", "edX / Linux Foundation", "Beginner", "https://www.edx.org/learn/linux/the-linux-foundation-introduction-to-linux"),
    ("Cloud Computing Basics", "Cloud", "AWS Skill Builder", "Beginner", "https://skillbuilder.aws/"),
    ("AWS Cloud Practitioner Essentials", "AWS", "AWS Skill Builder", "Beginner", "https://explore.skillbuilder.aws/"),
    ("DevOps Foundations", "DevOps", "Coursera", "Beginner", "https://www.coursera.org/learn/intro-to-devops"),
    ("Introduction to Cybersecurity", "Information Security", "Cisco Networking Academy", "Beginner", "https://www.netacad.com/courses/cybersecurity/introduction-cybersecurity"),
    ("Network Security Fundamentals", "Network Security", "Cisco NetAcad", "Beginner", "https://www.netacad.com/"),
    ("Ethical Hacking Essentials", "Ethical Hacking", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/news/ethical-hacking-course-for-beginners/"),
    ("Wireshark Packet Analysis", "Wireshark", "Wireshark Foundation", "Beginner", "https://www.wireshark.org/docs/"),
    ("Vulnerability Assessment", "Vulnerability Assessment", "Cybrary", "Beginner", "https://www.cybrary.it/"),
    ("Applied Cryptography", "Cryptography", "Stanford / Coursera", "Intermediate", "https://www.coursera.org/learn/crypto"),
    ("SIEM Basics & Security Monitoring", "SIEM", "Coursera", "Beginner", "https://www.coursera.org/"),
    ("Networking Basics", "Networking", "Cisco Networking Academy", "Beginner", "https://www.netacad.com/courses/packet-tracer/networking-basics"),
    ("TCP/IP Fundamentals", "TCP/IP", "Coursera", "Beginner", "https://www.coursera.org/learn/tcp-ip-fundamentals"),
    ("Routing and Switching Essentials", "Routing & Switching", "Cisco NetAcad", "Intermediate", "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html"),
    ("Cisco CCNA Prep", "Cisco", "Cisco NetAcad", "Beginner", "https://www.netacad.com/courses/ccna-introduction-networks"),
    ("Firewalls and Network Security", "Firewalls", "Palo Alto / Coursera", "Beginner", "https://www.coursera.org/"),
    ("Network Troubleshooting Guide", "Network Troubleshooting", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/"),
    ("Google UX Design Certificate", "UI/UX Design", "Coursera", "Beginner", "https://www.coursera.org/professional-certificates/google-ux-design"),
    ("Figma for UI/UX Design", "Figma", "Figma Learn", "Beginner", "https://help.figma.com/hc/en-us/categories/360002042553-Figma-for-beginners"),
    ("Wireframing & Prototyping Essentials", "Wireframing", "Interaction Design Foundation", "Beginner", "https://www.interaction-design.org/"),
    ("Interactive Prototyping", "Prototyping", "Coursera", "Beginner", "https://www.coursera.org/"),
    ("User Experience Research", "User Research", "edX / University of Michigan", "Beginner", "https://www.edx.org/"),
    ("Design Systems for Modern Apps", "Design Systems", "Figma", "Intermediate", "https://www.figma.com/design-systems/"),
    ("Android Basics in Kotlin", "Kotlin", "Android Developers", "Beginner", "https://developer.android.com/courses/android-basics-kotlin/course"),
    ("Android Studio Guide", "Android Studio", "Android Developers", "Beginner", "https://developer.android.com/studio/intro"),
    ("Android App Development", "Android SDK", "Google Developers", "Beginner", "https://developer.android.com/guide"),
    ("SQLite Tutorial", "SQLite", "SQLite.org", "Beginner", "https://www.sqlite.org/docs.html"),
    ("App Architecture (MVVM)", "MVVM", "Android Developers", "Intermediate", "https://developer.android.com/topic/architecture"),
    ("Software Testing Foundations", "Manual Testing", "Guru99", "Beginner", "https://www.guru99.com/software-testing.html"),
    ("Automation Testing with Selenium", "Automation Testing", "TestAutomationU", "Beginner", "https://testautomationu.applitools.com/"),
    ("Selenium WebDriver Guide", "Selenium", "Selenium.dev", "Beginner", "https://www.selenium.dev/documentation/"),
    ("API Testing with Postman", "API Testing", "Postman Academy", "Beginner", "https://academy.postman.com/"),
    ("Data Structures and Algorithms", "Data Structures", "freeCodeCamp", "Beginner", "https://www.freecodecamp.org/learn/"),
    ("Algorithms Specialization", "Algorithms", "Stanford / Coursera", "Intermediate", "https://www.coursera.org/specializations/algorithms"),
    ("Object-Oriented Programming Principles", "Object-Oriented Programming", "Coursera", "Beginner", "https://www.coursera.org/learn/object-oriented-java"),
    ("System Design Primer", "System Design", "GitHub", "Intermediate", "https://github.com/donnemartin/system-design-primer"),
    ("Web Security Fundamentals", "Web Security", "PortSwigger Web Security Academy", "Beginner", "https://portswigger.net/web-security"),
    ("Git Handbook", "Git", "GitHub Guides", "Beginner", "https://docs.github.com/en/get-started"),
    ("Django Web Framework Tutorial", "Django", "MDN Web Docs", "Beginner", "https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django"),
    ("Flask Tutorial", "Flask", "Pallets Projects", "Beginner", "https://flask.palletsprojects.com/tutorial/"),
    ("Bash Scripting Tutorial", "Bash", "Linux Journey", "Beginner", "https://linuxjourney.com/"),
    ("Computer Vision Basics", "Computer Vision", "Coursera", "Intermediate", "https://www.coursera.org/"),
    ("Production MLOps", "MLOps", "Made With ML", "Intermediate", "https://madewithml.com/"),
    ("Database Management Fundamentals", "Database Management", "Coursera", "Beginner", "https://www.coursera.org/learn/database-management")
]

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
            description TEXT DEFAULT '',
            display_order INTEGER DEFAULT 0
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

        # Add display_order column if upgrading an existing database
        try:
            db.execute("ALTER TABLE job_roles ADD COLUMN display_order INTEGER DEFAULT 0")
        except Exception:
            pass

        # 1. Seed or update Skills
        for skill_name, category in SKILL_CATEGORIES.items():
            db.execute("""
                INSERT INTO skills(skill_name, category) VALUES (?, ?)
                ON CONFLICT(skill_name) DO UPDATE SET category = excluded.category
            """, (skill_name, category))

        # 2. Seed or update Job Roles and their Role-Skills
        for role_item in ROLES_DATA:
            role_name = role_item["name"]
            desc = role_item["description"]
            order = role_item["order"]
            reqs = role_item["skills"]

            db.execute("""
                INSERT INTO job_roles(role_name, description, display_order)
                VALUES (?, ?, ?)
                ON CONFLICT(role_name) DO UPDATE SET
                    description = excluded.description,
                    display_order = excluded.display_order
            """, (role_name, desc, order))

            role_row = db.execute("SELECT role_id FROM job_roles WHERE role_name=?", (role_name,)).fetchone()
            role_id = role_row["role_id"]

            for skill, (level, weight) in reqs.items():
                cat = SKILL_CATEGORIES.get(skill, "Technical")
                db.execute("""
                    INSERT INTO skills(skill_name, category) VALUES (?, ?)
                    ON CONFLICT(skill_name) DO NOTHING
                """, (skill, cat))
                skill_id = db.execute("SELECT skill_id FROM skills WHERE skill_name=?", (skill,)).fetchone()["skill_id"]

                db.execute("""
                    INSERT INTO role_skills(role_id, skill_id, required_level, weight)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(role_id, skill_id) DO UPDATE SET
                        required_level = excluded.required_level,
                        weight = excluded.weight
                """, (role_id, skill_id, level, weight))

        # 3. Seed Course Recommendations
        for title, skill, provider, level, url in COURSE_CATALOG:
            s_row = db.execute("SELECT skill_id FROM skills WHERE skill_name=?", (skill,)).fetchone()
            if s_row:
                sid = s_row["skill_id"]
                db.execute("""
                    INSERT OR IGNORE INTO courses(title, skill_id, provider, level, url)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, sid, provider, level, url))

        db.commit()

if __name__ == "__main__":
    init_db()
    print("Database successfully initialized with 20 career roles and full skill mapping.")
