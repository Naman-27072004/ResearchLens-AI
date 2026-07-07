import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(question, vector_store, chunks, top_k=5):

    question_embedding = model.encode([question])

    distances, indices = vector_store.search(
        np.array(question_embedding).astype("float32"),
        top_k
    )

    retrieved_chunks = []

    for index in indices[0]:
        retrieved_chunks.append(chunks[index])

    return retrieved_chunks