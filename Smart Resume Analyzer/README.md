# 🧠 Smart Resume Analyzer (AI + Cloud Ready)

An end-to-end project to analyze resumes against job descriptions using embeddings and simple skill extraction. Built with **FastAPI**, **sentence-transformers**, and an optional **Streamlit** UI. Cloud-ready via **Docker** and **Cloud Run**.

---

## What You Will Demonstrate
- AI/NLP basics (embeddings, keyword/skill extraction).
- Software engineering (FastAPI API, tests, modular code).
- Cloud (Docker image + deploy to Google Cloud Run).
- Collaboration (Git + GitHub Actions template).
- Agile (Kanban tasks you can create in issues).

---

## 0) Prerequisites
- Python 3.11
- Git
- (Optional) Docker Desktop
- (Optional) Google Cloud account (for Cloud Run)

---

## 1) Quickstart (Local)

```bash
# 1. Clone or unzip this project
cd smart-resume-analyzer

# 2. Create venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install deps
pip install -r backend/requirements.txt

# 4. Run API (FastAPI + Uvicorn)
uvicorn backend.app.main:app --reload --port 8080

# 5. Open your browser: http://localhost:8080/docs  (interactive API docs)
```

### Streamlit UI (local, no API needed)
```bash
# In a new terminal with the venv activated:
streamlit run streamlit_app.py
# Opens a local web UI. Choose "Local (no API)".
```

---

## 2) How It Works (High-Level)
```
[Resume.pdf/.docx] --> text extraction --> clean --> embeddings  \
                                                           cosine similarity --> match score
[Job Description]  --> clean ---------> skill extraction --> compare skills --> missing/present
```

- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Skill extraction:** simple lookup from `skills/skills_master.csv` (you can extend it).
- **Outputs:** match score (0–100), skills present/missing, suggestions (no-LLM).

---

## 3) Project Structure
```
smart-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI endpoints
│   │   ├── model.py          # AnalyzerModel (embeddings + skills)
│   │   ├── utils.py          # PDF/DOCX/TXT extraction
│   │   └── schemas.py        # Pydantic response models
│   ├── tests/
│   │   └── test_basic.py     # pytest sanity test
│   ├── Dockerfile
│   └── requirements.txt
├── skills/
│   └── skills_master.csv     # extendable skills list
├── streamlit_app.py          # optional local UI
└── .github/
    └── workflows/
        └── deploy.yml        # GitHub Actions (Cloud Run)
```

---

## 4) API Usage

- **Health Check:** `GET /health`
- **Analyze:** `POST /analyze` (multipart form)
  - `resume`: file (PDF/DOCX/TXT)
  - `jd_text`: string

Try in your browser at `http://localhost:8080/docs`.

---

## 5) Run Tests
```bash
pytest -q
```

---

## 6) Docker Build & Run (Local)
```bash
# build
docker build -t resume-analyzer:latest -f backend/Dockerfile .

# run
docker run -p 8080:8080 resume-analyzer:latest

# open
# http://localhost:8080/health
# http://localhost:8080/docs
```

---

## 7) Deploy to Google Cloud Run (Free-ish, simple)

> Region tip for India: `asia-south1` (Mumbai).

1. Install/Init gcloud:
```bash
gcloud init
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID
gcloud auth configure-docker
```

2. Build container and push to Artifact Registry:
```bash
# create a repo (once):
gcloud artifacts repositories create resume-repo --repository-format=docker --location=asia-south1

# build & push
gcloud builds submit --tag asia-south1-docker.pkg.dev/YOUR_GCP_PROJECT_ID/resume-repo/resume-analyzer:v1 .
```

3. Deploy to Cloud Run:
```bash
gcloud run deploy resume-analyzer \
  --image asia-south1-docker.pkg.dev/YOUR_GCP_PROJECT_ID/resume-repo/resume-analyzer:v1 \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2
```

4. Get the URL from the output (e.g., `https://resume-analyzer-xxxx-as.a.run.app`) and use it in the Streamlit UI “Remote API” mode.

---

## 8) GitHub Actions CI/CD (Cloud Run)

- Add these **Repository → Settings → Secrets and variables → Actions → New repository secret**:
  - `GCP_PROJECT_ID` = your project id
  - `GCP_SA_KEY` = JSON key of a service account with Cloud Run + Cloud Build permissions
  - `GCP_REGION` = `asia-south1`
  - `ARTIFACT_REPO` = `resume-repo`

- Push to `main` branch to trigger deploy.

---

## 9) Extend for Bonus Points
- Add **LLM suggestions**: integrate OpenAI or local LLM for resume improvement tips.
- Replace skill extraction with **NER** (spaCy) or **keyword extraction** (YAKE/Rake).
- Add a simple **React UI** that calls the FastAPI endpoint.
- Persist results in a **database** (Postgres/Cloud SQL).
- Multi-resume batch scoring and **CSV export** for recruiters.
- JWT auth for a protected API.

---

## 10) Interview Talking Points
- Why embeddings (semantic vs keyword matching).
- Design choices (FastAPI for speed/dev experience, Cloud Run for simplicity).
- Tradeoffs (naive skills vs NER; LLM cost vs deterministic rules).
- Observability (health endpoint, unit tests; could add logging + metrics).

---

## Troubleshooting
- First run downloads the embedding model (~90MB). Keep internet on.
- If PDFs extract poorly, export resume as **text-based PDF** (not image scanned).
- On Cloud Run, increase memory/cpu if cold start feels slow.

---

**Good luck—ship it and show it!**
# Smart-Resume-Analyzer
# Smart-Resume-Analyzer
