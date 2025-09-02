# 🧠 Smart Resume Analyzer

An end-to-end project to analyze resumes against job descriptions using embeddings and skill extraction.  
Built with **FastAPI**, **sentence-transformers**, **Streamlit**, and deployed on **Google Cloud Run**.

---

## 🚀 Features
- Resume vs Job Description analysis
- Match score (0–100)
- Skills present & missing
- Suggestions for improvement
- Local UI via Streamlit
- Cloud deployment via Docker + Cloud Run

---

## ⚙️ Prerequisites
- Python 3.11
- Git
- Docker Desktop
- Google Cloud CLI (gcloud)

---

## 🖥️ Run Locally

### 1. Clone the Repo
```bash
git clone https://github.com/s-r2333/Smart-Resume-Analyzer.git
cd Smart-Resume-Analyzer
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Activate:
# Windows: .venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r backend/requirements.txt
```

### 4. Start API
```bash
uvicorn backend.app.main:app --reload --port 8080
```
Open: [http://localhost:8080/docs](http://localhost:8080/docs)

### 5. Start Streamlit App
```bash
streamlit run streamlit_app.py
```
Browser will open → choose **Local (no API)** to test.

---

## 🧪 Run Tests
```bash
pytest -q
```

---

## 🐳 Run with Docker

### Build Image
```bash
docker build -t resume-analyzer:latest -f backend/Dockerfile .
```

### Run Container
```bash
docker run -p 8080:8080 resume-analyzer:latest
```
Check: [http://localhost:8080/health](http://localhost:8080/health)

---

## ☁️ Deploy to Google Cloud Run

### 1. Authenticate
```bash
gcloud init
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth configure-docker
```

### 2. Create Artifact Repo & Push Image
```bash
gcloud artifacts repositories create resume-repo --repository-format=docker --location=asia-south1

gcloud builds submit --tag asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/resume-repo/resume-analyzer:v1 .
```

### 3. Deploy Service
```bash
gcloud run deploy resume-analyzer   --image asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/resume-repo/resume-analyzer:v1   --region asia-south1   --platform managed   --allow-unauthenticated   --port 8080   --memory 2Gi   --cpu 2
```

➡️ Get the public URL (e.g. `https://resume-analyzer-xxxx-as.a.run.app`)  
Use this in Streamlit under **Remote API** mode.

---

## 🔄 CI/CD with GitHub Actions
1. Go to **GitHub → Settings → Secrets → Actions**  
2. Add:
   - `GCP_PROJECT_ID`
   - `GCP_SA_KEY` (JSON key with Cloud Run + Build perms)
   - `GCP_REGION = asia-south1`
   - `ARTIFACT_REPO = resume-repo`
3. Push to **main** → automatic deploy.

---

## 💡 Interview Talking Points
- Built an **AI resume analyzer** using embeddings + skills.  
- Backend: **FastAPI**, Deployment: **Cloud Run**, CI/CD: **GitHub Actions**.  
- Containerized with **Docker** for portability.  
- Designed with observability & testing in mind.  

---

## 📂 Project Structure
```
smart-resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── model.py
│   │   ├── utils.py
│   │   └── schemas.py
│   ├── tests/
│   │   └── test_basic.py
│   ├── Dockerfile
│   └── requirements.txt
├── skills/
│   └── skills_master.csv
├── streamlit_app.py
└── .github/
    └── workflows/
        └── deploy.yml
```

---

✅ Follow this order and you’ll have a **working, deployable Smart Resume Analyzer**.
