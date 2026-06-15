from langchain_google_genai import ChatGoogleGenerativeAI
from src.prompt_templates import ATS_PROMPT


def analyze_resume(resume_text, job_description, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    prompt = ATS_PROMPT.format(
        resume=resume_text,
        job_description=job_description
    )

    response = llm.invoke(prompt)
    return response.content
