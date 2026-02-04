from fastapi import FastAPI, UploadFile, File
from typing import List
import tempfile

from resume_matcher import rank_resumes

app = FastAPI(title="AI Resume Screening System")

@app.post("/rank")
async def rank_candidates(
    resumes: List[UploadFile] = File(...),
    job_desc: str = ""
):
    resume_paths = {}

    for resume in resumes:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await resume.read())
            resume_paths[resume.filename] = tmp.name

    results = rank_resumes(resume_paths, job_desc)
    return {"ranked_candidates": results}
