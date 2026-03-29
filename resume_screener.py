from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def extract_keywords(text: str) -> set:
    \"\"\"Extract simple lowercase word tokens excluding basic stopwords.\"\"\"
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    stopwords = {'and', 'the', 'to', 'of', 'in', 'for', 'with', 'on', 'at', 'as', 'a', 'an', 'is', 'it', 'this', 'that', 'by', 'are'}
    words = text.split()
    return {w for w in words if w not in stopwords and len(w) > 3}

def calculate_resume_score(resume_text: str, job_description: str) -> dict:
    \"\"\"
    Enhanced TF-IDF based resume screening to match text against a job description.
    Also extracts missing keywords.
    Returns a dict with score and missing skills.
    \"\"\"
    if not resume_text or not job_description:
        return {"score": 0.0, "missing_keywords": []}
        
    documents = [job_description, resume_text]
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(similarity[0][0]) * 100
        score = round(score, 2)
        
        # Keyword gap analysis
        job_keywords = extract_keywords(job_description)
        resume_keywords = extract_keywords(resume_text)
        missing_skills = list(job_keywords - resume_keywords)[:5]
        
        return {"score": score, "missing_keywords": missing_skills}
    except ValueError:
        return {"score": 0.0, "missing_keywords": []}
