from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted


def extract_skills(text, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    prompt = f"""
    Extract skills from the following resume.

    Categorize them into:

    - Programming Languages
    - Frameworks
    - Databases
    - Cloud
    - Tools
    - Soft Skills

    Resume Text:
    {text}

    Return the result in clean markdown format.
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
        return f"Error extracting skills: {str(e)}"
