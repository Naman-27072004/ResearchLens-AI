import os
from dotenv import load_dotenv
import google.generativeai as genai

from backend.gap_prompt import create_gap_prompt

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def detect_research_gap(papers):

    if len(papers) < 2:
        return "Please upload at least two research papers."

    prompt = create_gap_prompt(papers)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 4096,
        },
    )

    return response.text