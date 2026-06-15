from langchain_google_genai import ChatGoogleGenerativeAI


def analyze_resume(resume_text, job_description, api_key):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.5-flash',
        google_api_key=api_key,
        temperature=0
    )

    prompt = f'''
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
    '''

    response = llm.invoke(prompt)
    return response.content
