from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted


def analyze_resume(resume_text, job_description, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    prompt = f"""
    Compare the resume against the job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:
    1. ATS Match Score (0-100)
    2. Matching Skills
    3. Missing Skills
    4. Short Improvement Suggestions
    """

    try:
        response = llm.invoke(prompt)
        return response.content

    except ResourceExhausted:
        return """
⚠️ Gemini API rate limit reached.

Please wait 1-2 minutes and try again.

Tip:
- Free tier has strict request limits.
- Avoid repeatedly refreshing the app.
        """

    except Exception as e:
        return f"Error analyzing resume: {str(e)}"
