import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_skills(text):
    skill_list = [
        "python", "django", "sql", "rest api", "machine learning",
        "pandas", "numpy", "excel", "html", "css", "javascript"
    ]
    text = text.lower()
    return [skill for skill in skill_list if skill in text]


def match_resume_to_jobs(resume_text, jobs):
    if not resume_text or not jobs.exists():
        return []

    resume_text = clean_text(resume_text)
    documents = [resume_text]
    valid_jobs = []

    for job in jobs:
        job_text = f"{job.description or ''} {job.skills or ''}"
        job_text = clean_text(job_text)
        if job_text:
            documents.append(job_text)
            valid_jobs.append(job)

    if len(documents) <= 1:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents)
    scores = cosine_similarity(vectors[0:1], vectors[1:])[0]

    resume_skills = extract_skills(resume_text)
    results = []
    for job, score in zip(valid_jobs, scores):
        job_skills = extract_skills(f"{job.description} {job.skills}")
        matched_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))
        results.append((job, round(score*100,2), matched_skills, missing_skills))

    return results
