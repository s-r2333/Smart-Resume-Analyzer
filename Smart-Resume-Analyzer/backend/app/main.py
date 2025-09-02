from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .utils import extract_text_from_file, clean_text
from .model import AnalyzerModel
from .schemas import AnalyzeResponse
import os

app = FastAPI(title="Smart Resume Analyzer", version="1.0")

# CORS for local dev & simple frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize model (path relative to backend/)
SKILLS_PATH = os.getenv("SKILLS_CSV_PATH", os.path.join(os.path.dirname(__file__), "../../skills/skills_master.csv"))
MODEL = AnalyzerModel(SKILLS_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(resume: UploadFile = File(...), jd_text: str = Form(...)):
    file_bytes = await resume.read()
    resume_text = clean_text(extract_text_from_file(file_bytes, resume.filename))
    jd_text_clean = clean_text(jd_text)

    if not resume_text.strip():
        return JSONResponse(status_code=400, content={"detail": "Could not read text from resume. Use PDF/DOCX/TXT."})

    result = MODEL.analyze(resume_text, jd_text_clean)
    return result
