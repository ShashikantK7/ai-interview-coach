import streamlit as st


def initialize_session():

    defaults = {
        "questions": [],
        "current_question": 0,
        "feedback_history": [],
        "answers": [],
        "scores": [],
        "interview_started": False,
        "interview_completed": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session():

    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.feedback_history = []
    st.session_state.answers = []
    st.session_state.scores = []
    st.session_state.interview_started = False
    st.session_state.interview_completed = False


def get_progress():

    total = len(st.session_state.questions)

    if total == 0:
        return 0

    return st.session_state.current_question / total


def is_last_question():

    return (
        st.session_state.current_question
        >= len(st.session_state.questions) - 1
    )


def average_score():

    if not st.session_state.scores:
        return 0

    return round(
        sum(st.session_state.scores)
        / len(st.session_state.scores),
        2
    )
