"""
Text Embeddings Generator

This module loads the SentenceTransformer model and computes vector representations 
(embeddings) of the extracted research paper text chunks.
"""

from sentence_transformers import SentenceTransformer

# Load model only once to optimize performance
model = SentenceTransformer("all-MiniLM-L6-v2")

import numpy as np

def create_embeddings(chunks: list[str]) -> np.ndarray:
    """
    Computes text embeddings for a list of document chunks.

    Args:
        chunks (list of str): List of text chunks extracted from the paper.

    Returns:
        numpy.ndarray: High-dimensional vector embeddings for each chunk.
    """
    embeddings = model.encode(chunks)
    return embeddings