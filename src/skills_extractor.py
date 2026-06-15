from langchain_google_genai import ChatGoogleGenerativeAI


def extract_skills(text, api_key):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    prompt = f"""
    Extract skills from the following text.

    Categorize them into:
    - Programming Languages
    - Frameworks
    - Databases
    - Cloud
    - Tools
    - Soft Skills

    Text:
    {text}
    """

    response = llm.invoke(prompt)
    return response.content
