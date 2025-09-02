from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class AnalyzerModel:
    """
    Wraps embeddings + simple skill extraction and match scoring.
    Downloads the embedding model on first use.
    """
    def __init__(self, skills_csv_path: str):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        skills_path = os.path.join(BASE_DIR, "skills", "skills_master.csv")
        self.skills = pd.read_csv(skills_path)["skill"].dropna().str.lower().str.strip().unique().tolist()

    def extract_skills(self, text: str) -> List[str]:
        text_l = text.lower()
        found = []
        for skill in self.skills:
            # exact word or simple containment (fast & simple)
            if skill in text_l:
                found.append(skill)
        # de-duplicate while preserving order
        seen = set()
        ordered = []
        for s in found:
            if s not in seen:
                ordered.append(s); seen.add(s)
        return ordered

    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)

    def match_score(self, resume_text: str, jd_text: str) -> float:
        E = self.embed([resume_text, jd_text])
        sim = float(cosine_similarity([E[0]], [E[1]])[0][0])
        # Scale to 0-100
        return round(sim * 100.0, 2)

    def analyze(self, resume_text: str, jd_text: str) -> Dict:
        rskills = set(self.extract_skills(resume_text))
        jskills = set(self.extract_skills(jd_text))

        score = self.match_score(resume_text, jd_text)

        missing = sorted(list(jskills - rskills))
        present = sorted(list(jskills & rskills))

        # naive suggestions (no LLM): focus on missing + keywords from JD
        suggestions = []
        if missing:
            suggestions.append(f"Consider learning or highlighting: {', '.join(missing[:10])}.")
        if score < 70:
            suggestions.append("Tailor your resume summary and projects to reflect the job's keywords and responsibilities.")
        if not suggestions:
            suggestions.append("Your resume aligns well. Add quantifiable impact (metrics) to strengthen it further.")

        return {
            "match_score": score,
            "jd_skills_detected": sorted(list(jskills)),
            "resume_skills_detected": sorted(list(rskills)),
            "skills_present_overlap": present,
            "skills_missing": missing,
            "suggestions": suggestions
        }
