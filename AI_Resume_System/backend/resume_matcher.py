import pdfplumber
from sentence_transformers import SentenceTransformer, util

# Load BERT model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Simple skill list
SKILLS = [
    "python", "java", "machine learning", "deep learning",
    "sql", "nlp", "data science", "tensorflow", "pytorch"
]

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text.lower()

def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return found

def skill_match_percentage(resume_skills, jd_text):
    jd_skills = extract_skills(jd_text.lower())
    if not jd_skills:
        return 0
    match = set(resume_skills).intersection(set(jd_skills))
    return len(match) / len(jd_skills)

def bert_similarity(resume_text, jd_text):
    r_emb = model.encode(resume_text)
    j_emb = model.encode(jd_text)
    return util.cos_sim(r_emb, j_emb).item()

def rank_resumes(resume_files, job_desc):
    results = []

    for filename, path in resume_files.items():
        text = extract_text_from_pdf(path)
        skills = extract_skills(text)

        bert_score = bert_similarity(text, job_desc)
        skill_score = skill_match_percentage(skills, job_desc)

        final_score = (0.6 * bert_score) + (0.4 * skill_score)

        results.append({
            "resume": filename,
            "bert_score": round(bert_score, 3),
            "skill_match": round(skill_score, 2),
            "final_score": round(final_score, 3),
            "skills": skills
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    for i, r in enumerate(results, start=1):
        r["rank"] = i

    return results
