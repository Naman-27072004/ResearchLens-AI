"""
Research Paper Summarizer Module

This module uses the Gemini LLM to construct structured, detailed executive summaries,
research objectives, key findings, keywords, limitations, gaps, and future scopes from 
the text of an uploaded paper.
"""

import os
import logging
from google import genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def analyze_paper(text: str) -> str:
    """
    Generates a structured research paper analysis/summary using Gemini.

    Args:
        text (str): The full raw text of the research paper.

    Returns:
        str: Markdown formatted executive summary, findings, limitations, and future scope.
    """

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

    try:
        logger.info("Sending paper analysis request to Gemini API.")
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        logger.info("Successfully received analysis response from Gemini API.")
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error during paper analysis: {e}", exc_info=True)
        raise e