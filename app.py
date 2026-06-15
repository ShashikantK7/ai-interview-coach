import streamlit as st

from src.config import GOOGLE_API_KEY
from src.resume_parser import extract_resume_text
from src.ats_analyzer import analyze_resume
from src.skills_extractor import extract_skills
from src.interview_generator import (
    generate_questions,
    generate_session_questions
)
from src.mock_interviewer import generate_interview_response
from src.interview_session import initialize_session
from src.score_tracker import extract_score

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

initialize_session()

st.title("🎯 AI Interview Coach")

st.caption(
    "Upload your resume, analyze ATS score, generate interview questions, and practice interviews."
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

            with st.spinner("Generating questions..."):

                questions = generate_questions(
                    extracted_skills,
                    GOOGLE_API_KEY
                )

            st.markdown(questions)

    with tab4:

        st.subheader("AI Mock Interview")

        if not st.session_state.interview_started:

            if st.button("Start Mock Interview"):

                with st.spinner(
                    "Preparing interview questions..."
                ):

                    st.session_state.questions = (
                        generate_session_questions(
                            extracted_skills,
                            GOOGLE_API_KEY
                        )
                    )

                    st.session_state.current_question = 0
                    st.session_state.feedback_history = []
                    st.session_state.answers = []
                    st.session_state.scores = []
                    st.session_state.interview_started = True

                st.rerun()

        else:

            total_questions = len(
                st.session_state.questions
            )

            current_index = (
                st.session_state.current_question
            )

            st.progress(
                (current_index + 1)
                / total_questions
            )

            st.write(
                f"Question {current_index + 1} "
                f"of {total_questions}"
            )

            current_question = (
                st.session_state.questions[
                    current_index
                ]
            )

            st.info(current_question)

            answer = st.text_area(
                "Your Answer",
                key=f"answer_{current_index}",
                height=180
            )

            if st.button(
                "Submit Answer",
                key=f"submit_{current_index}"
            ):

                if answer:

                    with st.spinner(
                        "Evaluating answer..."
                    ):

                        feedback = (
                            generate_interview_response(
                                current_question,
                                answer,
                                GOOGLE_API_KEY
                            )
                        )

                    score = extract_score(
                        feedback
                    )

                    st.session_state.answers.append(
                        answer
                    )

                    st.session_state.feedback_history.append(
                        feedback
                    )

                    st.session_state.scores.append(
                        score
                    )

                    st.markdown(feedback)

                    if (
                        current_index
                        < total_questions - 1
                    ):

                        if st.button(
                            "Next Question"
                        ):

                            st.session_state.current_question += 1
                            st.rerun()

                    else:

                        st.success(
                            "Interview Completed!"
                        )

                        avg_score = round(
                            sum(
                                st.session_state.scores
                            )
                            / len(
                                st.session_state.scores
                            ),
                            2
                        )

                        st.metric(
                            "Average Score",
                            f"{avg_score}/10"
                        )

                        st.subheader(
                            "Question Scores"
                        )

                        for i, score in enumerate(
                            st.session_state.scores,
                            start=1
                        ):
                            st.write(
                                f"Q{i}: {score}/10"
                            )

                else:
                    st.warning(
                        "Please enter your answer."
                    )
