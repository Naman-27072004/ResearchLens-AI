import numpy as np
import faiss
from backend.retriever import retrieve_chunks

def test_retrieve_chunks():
    chunks = [
        "The quick brown fox jumps over the lazy dog.",
        "Deep learning is a subset of machine learning.",
        "Research Lens AI uses RAG models for paper analysis.",
        "FAISS is an efficient library for dense vector search.",
        "Generative artificial intelligence has evolved quickly."
    ]
    
    # We will mock the FAISS index to return specific indices when search is called
    class MockVectorStore:
        def search(self, query_vector, k):
            # return indices [2, 3] representing chunk 2 and 3
            distances = np.array([[0.1, 0.2]], dtype="float32")
            indices = np.array([[2, 3]], dtype="int64")
            return distances, indices

    mock_index = MockVectorStore()
    results = retrieve_chunks("RAG models", mock_index, chunks, top_k=2)
    assert len(results) == 2
    assert results[0] == "Research Lens AI uses RAG models for paper analysis."
    assert results[1] == "FAISS is an efficient library for dense vector search."
