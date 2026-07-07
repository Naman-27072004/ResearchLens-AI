"""
Research Paper Comparison Module

This module compares multiple research papers using the Gemini model. It sets up 
the API configuration, prompts Gemini to identify similarities, differences, 
methodology variances, strengths, and weaknesses across papers, and returns a formatted comparison.
"""

import os
import logging
from dotenv import load_dotenv
from typing import Any
from google import genai
from google.genai import types

from backend.comparison_prompt import create_comparison_prompt

load_dotenv()

logger = logging.getLogger(__name__)
client = genai.Client()


def compare_papers(papers: list[dict[str, Any]]) -> str:
    """
    Compare multiple research papers using Gemini.
    """

    # Validate input
    if len(papers) < 2:
        logger.warning("Attempted to compare less than 2 papers.")
        return "⚠️ Please upload at least two research papers for comparison."

    logger.info(f"Generating prompt to compare {len(papers)} papers.")
    # Create prompt
    prompt = create_comparison_prompt(papers)

    # Generate response
    try:
        logger.info("Sending comparison query to Gemini API.")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                max_output_tokens=4096,
            ),
        )
        logger.info("Successfully received comparison response from Gemini API.")
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error during paper comparison: {e}", exc_info=True)
        raise e