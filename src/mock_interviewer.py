from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted


def generate_interview_response(question, answer, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )

    prompt = f"""
    You are an experienced technical interviewer.

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Evaluate the answer.

    Provide:
    1. Score out of 10
    2. Strengths
    3. Areas for Improvement
    4. Sample Better Answer

    Return clean markdown.
    """

    try:
        response = llm.invoke(prompt)
        return response.content
    except ResourceExhausted:
        return "Gemini API rate limit reached. Please try again in a minute."
    except Exception as e:
        return f"Error evaluating answer: {str(e)}"
