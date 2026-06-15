from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted


def generate_questions(skills_text, api_key):
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
