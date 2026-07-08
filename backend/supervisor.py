"""
Supervisor Agent Module

This module implements a router/supervisor agent that classifies and routes
a user's query to the most appropriate backend agent (summary, chat, comparison,
research_gap, or citation).
"""

import os
import logging
from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)


def route_query(user_query: str) -> str:
    """
    Classifies a user query and routes it to one of the five specific research agents.

    Args:
        user_query (str): The natural language query from the user.

    Returns:
        str: The name of the selected agent (one of: 'summary', 'chat', 'comparison', 'research_gap', 'citation').
    """

    client = genai.Client()

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

    try:
        logger.info("Sending supervisor routing query to Gemini API.")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        routed_agent = response.text.strip().lower()
        logger.info(f"Supervisor routed user query to agent: {routed_agent}")
        return routed_agent
    except Exception as e:
        logger.error(f"Gemini API error during supervisor routing: {e}", exc_info=True)
        raise e