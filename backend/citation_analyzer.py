import re
from collections import Counter


def extract_references(text):
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


def author_statistics(references):
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


def citation_analysis(text):

    references = extract_references(text)

    stats = author_statistics(references)

    return {
        "total_references": len(references),
        "references": references,
        "top_authors": stats,
    }