"""
Citation Analysis Module

This module extracts the references or bibliography section from academic papers,
identifies referenced authors, and performs basic citation analytics (e.g., citation count
and top cited author statistics).
"""

import re
from collections import Counter
from typing import Any


def extract_references(text: str) -> list[str]:
    """
    Extract the References/Bibliography section from a research paper.
    """

    patterns = [
        r"(?i)\breferences\b",
        r"(?i)\bbibliography\b",
        r"(?i)\bworks cited\b"
    ]

    start = None

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            start = match.start()
            break

    if start is None:
        return []

    references_text = text[start:]

    references = []

    for line in references_text.split("\n"):

        line = line.strip()

        if len(line) > 20:
            references.append(line)

    return references


def author_statistics(references: list[str]) -> list[tuple[str, int]]:
    """
    Count author surnames appearing in references.
    """

    authors = []

    for ref in references:

        # Very simple surname extraction
        matches = re.findall(r"\b[A-Z][a-zA-Z'-]+\b", ref)

        if matches:
            authors.append(matches[0])

    return Counter(authors).most_common(10)


def citation_analysis(text: str) -> dict[str, Any]:
    """
    Performs unified citation analysis on the text of a research paper.

    Args:
        text (str): The full raw text of the research paper.

    Returns:
        dict: A dictionary containing:
            - "total_references" (int): The number of extracted references.
            - "references" (list of str): List of raw reference lines.
            - "top_authors" (list of tuple): Top 10 most common author surnames and counts.
    """

    references = extract_references(text)

    stats = author_statistics(references)

    return {
        "total_references": len(references),
        "references": references,
        "top_authors": stats,
    }