import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def route_query(user_query):

    prompt = f"""
You are a Supervisor AI responsible for routing user requests.

Available agents:

1. summary
   - Summarize a research paper
   - Explain objectives, methodology, results

2. chat
   - Answer questions using the uploaded paper

3. comparison
   - Compare multiple research papers

4. research_gap
   - Find research gaps
   - Suggest future work
   - Identify limitations

5. citation
   - Analyze references
   - Citation analytics

Rules:
- Return ONLY one word.
- No explanation.
- Choose from:
summary
chat
comparison
research_gap
citation

User Request:
{user_query}
"""

    response = model.generate_content(prompt)

    return response.text.strip().lower()