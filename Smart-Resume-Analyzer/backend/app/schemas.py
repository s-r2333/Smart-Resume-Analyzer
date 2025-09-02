from pydantic import BaseModel, Field
from typing import List

class AnalyzeResponse(BaseModel):
    match_score: float = Field(..., description="0-100 similarity score between resume and JD")
    jd_skills_detected: List[str]
    resume_skills_detected: List[str]
    skills_present_overlap: List[str]
    skills_missing: List[str]
    suggestions: List[str]
