"""
Information Retrieval Module

This module embeds the user's question and performs a semantic search against
a FAISS vector index to retrieve the most relevant text chunks from the research paper.
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Load model only once to optimize performance
model = SentenceTransformer("all-MiniLM-L6-v2")

from typing import Any

def retrieve_chunks(question: str, vector_store: Any, chunks: list[str], top_k: int = 5) -> list[str]:
    """
    Performs a vector similarity search to find the most relevant document chunks for a question.

    Args:
        question (str): The research question/query from the user.
        vector_store (faiss.Index): The FAISS index holding the chunk embeddings.
        chunks (list of str): The actual raw text chunks mapping to index positions.
        top_k (int, optional): The number of most relevant chunks to retrieve. Defaults to 5.

    Returns:
        list of str: The top_k most similar text chunks.
    """

    question_embedding = model.encode([question])

    distances, indices = vector_store.search(
        np.array(question_embedding).astype("float32"),
        top_k
    )

    retrieved_chunks = []

    for index in indices[0]:
        retrieved_chunks.append(chunks[index])

    return retrieved_chunks