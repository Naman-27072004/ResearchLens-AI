"""
Vector Store Module

This module constructs an in-memory vector database using FAISS to index 
high-dimensional embeddings, allowing for fast similarity searches.
"""

import logging
from typing import Any
import faiss
import numpy as np

logger = logging.getLogger(__name__)

def create_vector_store(embeddings: np.ndarray) -> Any:
    """
    Creates and populates a FAISS IndexFlatL2 vector index with document embeddings.

    Args:
        embeddings (numpy.ndarray): The calculated high-dimensional embeddings for the text chunks.

    Returns:
        faiss.IndexFlatL2: A populated FAISS flat vector index for L2 distance matching.
    """
    logger.info("Initializing FAISS flat L2 vector index.")
    try:
        if embeddings.ndim < 2:
            raise ValueError(f"Embeddings array must be 2-dimensional, got shape {embeddings.shape}")
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype("float32"))
        logger.info(f"Successfully added {index.ntotal} vectors of dimension {dimension} to index.")
        return index
    except Exception as e:
        logger.error(f"Error creating FAISS vector store: {e}", exc_info=True)
        raise e