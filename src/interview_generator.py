from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted


def generate_questions(skills_text, api_key):
    """
    Existing Phase 3 feature:
    Generate categorized interview questions.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )

    prompt = f"""
    You are an experienced technical interviewer.

    Candidate skills:

    {skills_text}

    Generate:

    1. Beginner interview questions
    2. Intermediate interview questions
    3. Advanced interview questions
    4. Behavioral interview questions

    Return clean markdown.
    """

    try:
        response = llm.invoke(prompt)
        return response.content

    except ResourceExhausted:
        return "Gemini API rate limit reached. Please try again in a minute."

    except Exception as e:
        return f"Error generating questions: {str(e)}"


def generate_session_questions(skills_text, api_key):
    """
    Phase 4.3:
    Generate exactly 5 interview questions
    for a guided mock interview session.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.4
    )

    prompt = f"""
    You are a senior technical interviewer.

    Candidate skills:

    {skills_text}

    Generate EXACTLY 5 interview questions.

    Requirements:
    - Questions should be relevant to the candidate skills.
    - Mix beginner, intermediate, advanced, and behavioral questions.
    - One question per line.
    - Do NOT include numbering.
    - Do NOT include explanations.
    - Output only the questions.

    Example:

    What is overfitting in machine learning?
    Explain the difference between Random Forest and XGBoost.
    How does backpropagation work?
    Describe a challenging project you worked on.
    How would you deploy a machine learning model to production?
    """

    try:
        response = llm.invoke(prompt)

        questions = [
            q.strip()
            for q in response.content.split("\n")
            if q.strip()
        ]

        return questions[:5]

    except ResourceExhausted:
        return [
            "Gemini API rate limit reached. Please try again in a minute."
        ]

    except Exception as e:
        return [
            f"Error generating interview session: {str(e)}"
        ]
