import numpy as np
from backend.vectorstore import create_vector_store

def test_create_vector_store():
    # Create random embeddings of shape (5, 384)
    embeddings = np.random.rand(5, 384).astype("float32")
    index = create_vector_store(embeddings)
    assert index.ntotal == 5
    assert index.d == 384
