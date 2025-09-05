from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .utils import extract_text_from_file, clean_text
from .model import AnalyzerModel
from .schemas import AnalyzeResponse
import os

app = FastAPI(
    title="Smart Resume Analyzer API",
    description="🚀 Backend service that analyzes resumes against job descriptions using NLP and skill-matching.",
    version="1.0",
    openapi_url="/schema.json",   # 👈 replaces /openapi.json
    docs_url="/docs",             # Swagger UI stays at /docs
    redoc_url=None                # Disable ReDoc if not needed
)

# CORS for local dev & simple frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model (path relative to backend/)
SKILLS_PATH = os.getenv(
    "SKILLS_CSV_PATH",
    os.path.join(os.path.dirname(__file__), "../../skills/skills_master.csv")
)
MODEL = AnalyzerModel(SKILLS_PATH)


@app.get("/health", summary="Health Check")
def health():
    """Quick check to confirm the API is running."""
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse, summary="Analyze Resume vs JD")
async def analyze(resume: UploadFile = File(...), jd_text: str = Form(...)):
    """
    Upload a resume (PDF/DOCX/TXT) and a job description (JD).
    The API will return skill matches, missing skills, and a score.
    """
    file_bytes = await resume.read()
    resume_text = clean_text(extract_text_from_file(file_bytes, resume.filename))
    jd_text_clean = clean_text(jd_text)

    if not resume_text.strip():
        return JSONResponse(
            status_code=400,
            content={"detail": "Could not read text from resume. Use PDF/DOCX/TXT."}
        )

    result = MODEL.analyze(resume_text, jd_text_clean)
    return result
