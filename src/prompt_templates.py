ATS_PROMPT = """
Compare the resume against the job description.

Resume:
{resume}

Job Description:
{job_description}

Return the result in this format:

ATS Match Score: <score>/100

Matching Skills:
- ...

Missing Skills:
- ...

Strengths:
- ...

Weaknesses:
- ...

Improvement Suggestions:
- ...
"""
