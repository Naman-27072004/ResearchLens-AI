"""
Comparison Prompt Generator

This module constructs a highly detailed comparison prompt for the Gemini LLM
to review, compare, and contrast multiple academic research papers, including
producing comparison tables, identifying similarities/differences, and highlighting gaps.
"""

from typing import Any

def create_comparison_prompt(papers: list[dict[str, Any]]) -> str:
    """
    Creates a detailed comparison prompt for multiple research papers.

    Args:
        papers (list of dict): A list of dictionaries representing the uploaded papers.
            Each dictionary should contain 'name' and 'text'.

    Returns:
        str: The fully constructed prompt containing instructions and papers' text.
    """

    prompt = """
You are an expert Research Scientist and Peer Reviewer.

You have been provided with MULTIPLE research papers.

Your task is to COMPARE the papers, NOT summarize just one paper.

IMPORTANT RULES:
1. Read ALL papers before answering.
2. Mention every paper by its filename.
3. Compare every paper with the others.
4. Do NOT write individual summaries.
5. Highlight similarities and differences.
6. If only one paper is provided, clearly say:
   "Only one paper was provided. Comparison requires at least two papers."

Return your response in the following format.

# Research Paper Comparison

## 1. Comparison Table

| Paper | Objective | Methodology | Dataset | Model | Results | Strengths | Weaknesses |
|------|-----------|------------|---------|-------|----------|------------|-------------|

Fill one row for every paper.

---

## 2. Similarities

Mention common ideas, datasets, architectures, or goals.

---

## 3. Differences

Explain how the papers differ in:
- Methodology
- Algorithms
- Models
- Dataset
- Evaluation
- Performance

---

## 4. Best Performing Paper

State which paper appears strongest and explain why.

---

## 5. Research Gaps

Identify:
- Missing experiments
- Limitations
- Future work opportunities
- Unexplored research directions

---

Below are the research papers.

"""

    for i, paper in enumerate(papers, start=1):

        prompt += f"""

==========================================================
PAPER {i}

Filename:
{paper['name']}

Content:
{paper['text'][:6000]}

==========================================================

"""

    return prompt