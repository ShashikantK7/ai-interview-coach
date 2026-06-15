import streamlit as st

from src.config import GOOGLE_API_KEY
from src.resume_parser import extract_resume_text
from src.ats_analyzer import analyze_resume
from src.skills_extractor import extract_skills
from src.interview_generator import generate_questions
from src.mock_interviewer import generate_interview_response

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Interview Coach")
st.caption(
    "Upload your resume, compare it with a job description, generate interview questions, and practice answers."
)

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

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "ATS Analysis",
            "Extracted Skills",
            "Interview Questions",
            "Mock Interview"
        ]
    )

    with tab1:
        st.subheader("ATS Analysis")
        st.markdown(ats_result)

    with tab2:
        st.subheader("Skills Found In Resume")
        st.markdown(extracted_skills)

    with tab3:
        st.subheader("Interview Questions")

        if st.button("Generate Interview Questions"):
            with st.spinner("Generating interview questions..."):
                questions = generate_questions(
                    extracted_skills,
                    GOOGLE_API_KEY
                )
            st.markdown(questions)

    with tab4:
        st.subheader("Mock Interview Practice")

        question = st.text_input(
            "Interview Question",
            placeholder="What is overfitting in machine learning?"
        )

        answer = st.text_area(
            "Your Answer",
            height=180
        )

        if st.button("Evaluate Answer"):
            if question and answer:
                with st.spinner("Evaluating answer..."):
                    feedback = generate_interview_response(
                        question,
                        answer,
                        GOOGLE_API_KEY
                    )

                st.markdown(feedback)
            else:
                st.warning("Please enter both a question and an answer.")