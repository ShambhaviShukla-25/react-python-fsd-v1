from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import io
import docx2txt
import PyPDF2
import re

app = FastAPI()

# Allow frontend (Netlify) to access backend (Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample skill set
SKILLS = [
    "Python", "JavaScript", "Java", "C++", "React", "Node.js", "Django",
    "FastAPI", "SQL", "MongoDB", "Machine Learning", "HTML", "CSS", "Git", "REST API"
]

def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    content = io.BytesIO(file.file.read())
    return docx2txt.process(content)

@app.post("/extract-skills/")
async def extract_skills(file: UploadFile = File(...)):
    text = ""
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return {"error": "Unsupported file type"}

    text_lower = text.lower()
    found_skills = [skill for skill in SKILLS if skill.lower() in text_lower]
    return {"skills": list(set(found_skills))}
