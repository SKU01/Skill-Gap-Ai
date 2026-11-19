import re
from functools import lru_cache

SKILL_TERMS = [
    # Programming & Scripting
    "Python", "Java", "JavaScript", "TypeScript", "Kotlin", "PHP", "C++", "C", "R", "Bash", "SQL",
    # Web & Full Stack
    "HTML", "CSS", "React", "Node.js", "Express", "Django", "Flask", "Spring Boot", "Hibernate",
    "REST APIs", "Microservices", "Responsive Design", "Web Security",
    # Data & AI / ML
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "Computer Vision",
    "Generative AI", "Large Language Models", "Scikit-learn", "PyTorch", "TensorFlow", "MLOps",
    "Data Analysis", "Data Visualization", "Power BI", "Tableau", "Excel", "Statistics", "Mathematics",
    "Pandas", "NumPy",
    # Databases & Storage
    "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Oracle", "Database Administration",
    "Database Management", "Data Modeling", "Performance Tuning", "Backup & Recovery",
    # Cloud, DevOps & Tools
    "Cloud", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Terraform",
    "Linux", "DevOps", "Git", "GitHub",
    # Cybersecurity & Networking
    "Network Security", "Information Security", "Ethical Hacking", "Wireshark", "Cryptography",
    "SIEM", "Vulnerability Assessment", "Networking", "TCP/IP", "Routing & Switching", "Cisco",
    "Firewalls", "Network Troubleshooting",
    # Mobile
    "Android Studio", "Android SDK", "MVVM",
    # QA & Testing
    "Manual Testing", "Automation Testing", "Selenium", "API Testing", "JIRA", "Agile",
    # Architecture, BA & UI/UX
    "Data Structures", "Algorithms", "Object-Oriented Programming", "System Design",
    "Business Analysis", "Requirements Gathering", "Communication",
    "UI/UX Design", "Figma", "Wireframing", "Prototyping", "User Research", "Design Systems"
]

def extract_skills(text):
    """spaCy PhraseMatcher skill extraction; falls back to case-insensitive matching."""
    found = set()
    term_map = {t.lower(): t for t in SKILL_TERMS}
    try:
        import spacy
        from spacy.matcher import PhraseMatcher
        nlp = spacy.blank("en")
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        matcher.add("SKILLS", [nlp.make_doc(s) for s in SKILL_TERMS])
        doc = nlp(text[:200000])
        for _, start, end in matcher(doc):
            matched_lower = doc[start:end].text.lower()
            found.add(term_map.get(matched_lower, doc[start:end].text))
    except Exception:
        lower = text.lower()
        for term in SKILL_TERMS:
            if re.search(r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)", lower):
                found.add(term)
    return sorted(found, key=str.lower)

@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def semantic_match(extracted, required):
    """
    Sentence-BERT cosine similarity maps resume skill phrases to role skills.
    If the model is unavailable (e.g. first run without internet), use exact
    case-insensitive matching so the rest of the project remains usable.
    """
    if not extracted:
        return {}
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        model = _model()
        emb_a = model.encode(extracted, normalize_embeddings=True)
        emb_b = model.encode(required, normalize_embeddings=True)
        sims = cosine_similarity(emb_b, emb_a)
        result = {}
        for i, req in enumerate(required):
            best_idx = int(sims[i].argmax())
            result[req] = float(sims[i][best_idx])
        return result
    except Exception:
        ext_lower = [x.lower() for x in extracted]
        return {req: (1.0 if req.lower() in ext_lower else 0.0)
                for req in required}
