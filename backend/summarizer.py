import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_paper(text):

    prompt = f"""
You are an expert research assistant.

Analyze this paper.

Return your answer in Markdown.

Include:

# Executive Summary

# Research Objective

# Key Findings

# Keywords

# Limitations

# Research Gaps

# Future Scope

Paper:

{text[:12000]}
"""

    response = model.generate_content(prompt)

    return response.text