# Simple CPU image for FastAPI + sentence-transformers
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for pdfplumber (poppler-utils fonts) & docx2txt
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    poppler-utils \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Download the embedding model at build time (optional, speeds cold start)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

COPY skills /app/skills
COPY backend /app/backend

EXPOSE 8080
# Uvicorn on Cloud Run prefers 0.0.0.0:8080
CMD [\"uvicorn\", \"backend.app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8080\"]
