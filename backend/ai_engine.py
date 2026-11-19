import re
from functools import lru_cache

SKILL_TERMS = [
    "Python","SQL","Machine Learning","Cloud","Communication","Excel","Statistics",
    "Data Visualization","Power BI","Git","HTML","JavaScript","CSS","Flask","React",
    "Data Analysis","Deep Learning","Artificial Intelligence","NLP","MySQL","SQLite"
]

def extract_skills(text):
    """spaCy PhraseMatcher skill extraction; falls back to case-insensitive matching."""
    found = set()
    try:
        import spacy
        from spacy.matcher import PhraseMatcher
        nlp = spacy.blank("en")
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        matcher.add("SKILLS", [nlp.make_doc(s) for s in SKILL_TERMS])
        doc = nlp(text[:200000])
        for _, start, end in matcher(doc):
            found.add(doc[start:end].text)
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
        return {req: (1.0 if req.lower() in [x.lower() for x in extracted] else 0.0)
                for req in required}
