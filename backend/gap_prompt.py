"""
Gap Prompt Generator

This module constructs a highly structured analysis prompt for the Gemini LLM
to identify themes, shared limitations, research gaps, and generate novel 
research ideas across multiple uploaded papers.
"""

from typing import Any

def create_gap_prompt(papers: list[dict[str, Any]]) -> str:
    """
    Creates a detailed gap detection prompt for multiple research papers.

    Args:
        papers (list of dict): A list of dictionaries representing the uploaded papers.
            Each dictionary should contain 'name' and 'text'.

    Returns:
        str: The fully constructed prompt containing instructions and papers' text.
    """

    prompt = """
You are a senior research reviewer.

You have been given MULTIPLE research papers.

Your task is NOT to summarize each paper.

Instead, compare all papers together and identify research opportunities.

IMPORTANT RULES:
- Do NOT write "Paper 1", "Paper 2", etc.
- Do NOT summarize each paper individually.
- Read all papers before answering.
- Focus only on identifying gaps across the papers.

Return your answer in the following format:

# Common Themes

List the research topics that are common across the papers.

---

# Common Limitations

Identify limitations shared by multiple papers.

---

# Research Gaps

Identify what existing research has NOT addressed.

Examples:
- Missing datasets
- Lack of real-world evaluation
- No scalability analysis
- No explainability
- Small datasets
- Limited performance metrics
- Lack of deployment

---

# Future Research Directions

Suggest improvements and future work.

---

# Novel Research Ideas

Suggest 5 innovative research project ideas based on the identified gaps.

Below are the papers.

"""

    for i, paper in enumerate(papers, start=1):

        prompt += f"""

=========================
Paper {i}

Filename: {paper['name']}

Content:

{paper['text'][:5000]}

"""

    return prompt