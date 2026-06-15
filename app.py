import streamlit as st
from src.config import GOOGLE_API_KEY
from src.resume_parser import extract_resume_text
from src.ats_analyzer import analyze_resume
from src.skills_extractor import extract_skills

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯"
)

st.title("🎯 AI Interview Coach")
st.caption("Upload your resume and compare it against a job description")

if not GOOGLE_API_KEY:
    st.error("Google API key not configured.")
    st.stop()

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if resume_file and job_description:

    with st.spinner("Reading resume..."):
        resume_text = extract_resume_text(resume_file)

    with st.spinner("Extracting skills..."):
        extracted_skills = extract_skills(
            resume_text,
            GOOGLE_API_KEY
        )

    with st.spinner("Analyzing ATS match..."):
        ats_result = analyze_resume(
            resume_text,
            job_description,
            GOOGLE_API_KEY
        )

    st.success("Analysis complete!")

    tab1, tab2 = st.tabs(
        ["ATS Analysis", "Extracted Skills"]
    )

    with tab1:
        st.subheader("ATS Analysis")
        st.markdown(ats_result)

    with tab2:
        st.subheader("Skills Found In Resume")
        st.markdown(extracted_skills)
