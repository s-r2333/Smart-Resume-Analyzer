from backend.app.model import AnalyzerModel

def test_basic_scoring():
    model = AnalyzerModel("skills/skills_master.csv")
    resume = "Experienced Python developer with FastAPI and AWS. Built ML pipelines with scikit-learn."
    jd = "Looking for a developer skilled in Python, FastAPI, AWS and CI/CD."
    res = model.analyze(resume, jd)
    assert 0 <= res["match_score"] <= 100
    assert set(["python", "fastapi", "aws"]).issubset(set(res["resume_skills_detected"]) | set(res["jd_skills_detected"]))
