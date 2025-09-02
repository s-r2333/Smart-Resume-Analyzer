import streamlit as st
import requests
from backend.app.utils import extract_text_from_file, clean_text
from backend.app.model import AnalyzerModel
import os

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🧠")

st.title("🧠 Smart Resume Analyzer")
st.caption("Analyze resume vs job description. Local mode or via FastAPI API.")

mode = st.radio("Mode", ["Local (no API)", "Remote API"], horizontal=True)
api_url = st.text_input("API URL (for Remote API mode)", value="http://127.0.0.1:8080")
resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
jd_text = st.text_area("Paste Job Description", height=200, placeholder="Paste the JD here...")

if st.button("Analyze", disabled=not resume_file or not jd_text.strip()):
    with st.spinner("Analyzing..."):
        if mode == "Remote API":
            files = {"resume": (resume_file.name, resume_file.getvalue())}
            data = {"jd_text": jd_text}
            r = requests.post(f"{api_url.rstrip('/')}/analyze", files=files, data=data, timeout=120)
            if r.ok:
                result = r.json()
            else:
                st.error(r.text)
                st.stop()
        else:
            # Local mode uses the same pipeline without the API
            MODEL = AnalyzerModel("skills/skills_master.csv")
            text = clean_text(extract_text_from_file(resume_file.getvalue(), resume_file.name))
            result = MODEL.analyze(text, jd_text)

    st.subheader("Results")
    st.metric("Match Score", f"{result['match_score']} / 100")
    st.write("**JD Skills Detected:**", ", ".join(result["jd_skills_detected"]) or "—")
    st.write("**Resume Skills Detected:**", ", ".join(result["resume_skills_detected"]) or "—")
    st.write("**Overlap (present):**", ", ".join(result["skills_present_overlap"]) or "—")
    st.write("**Missing Skills:**", ", ".join(result["skills_missing"]) or "—")
    st.write("**Suggestions:**")
    for s in result["suggestions"]:
        st.write("- ", s)
