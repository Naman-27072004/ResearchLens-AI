"""
Text Chunking Module

This module handles splitting large documents into smaller, overlapping chunks
to prepare them for text embedding generation and vector database indexing.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text: str) -> list[str]:
    """
    Splits the input text into smaller chunks using a recursive character splitter.

    Args:
        text (str): The raw text extracted from a research paper.

    Returns:
        list of str: A list of text chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    return chunks