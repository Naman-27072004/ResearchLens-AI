import os
from dotenv import load_dotenv
import google.generativeai as genai

from backend.comparison_prompt import create_comparison_prompt

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def compare_papers(papers):
    """
    Compare multiple research papers using Gemini.
    """

    # Validate input
    if len(papers) < 2:
        return "⚠️ Please upload at least two research papers for comparison."

    # Create prompt
    prompt = create_comparison_prompt(papers)

    # Generate response
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.9,
            "max_output_tokens": 4096,
        },
    )

    return response.text