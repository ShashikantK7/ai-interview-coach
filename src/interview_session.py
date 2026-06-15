import streamlit as st


def initialize_session():
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "feedback_history" not in st.session_state:
        st.session_state.feedback_history = []

    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
