"""
Retrieval-Augmented Generation (RAG) Module

This module takes a user query and the most relevant chunks retrieved from the paper
and uses the Gemini LLM to generate a contextually restricted, detailed answer.
"""

import os
import logging
from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)
client = genai.Client()


def answer_question(question: str, retrieved_chunks: list[str]) -> str:
    """
    Answers a user question based strictly on the retrieved research paper text chunks.

    Args:
        question (str): The research-related question asked by the user.
        retrieved_chunks (list of str): Chunks of text containing relevant background information.

    Returns:
        str: The AI-generated answer or a fallback message if not found in the context.
    """

    logger.info(f"Answering question using {len(retrieved_chunks)} context chunks.")
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an AI Research Assistant.

Answer ONLY using the provided research paper context.

If the answer is not present in the context, say:

"I couldn't find this information in the uploaded paper."

Context:

{context}

Question:

{question}

Provide a detailed but concise answer.
"""

    try:
        logger.info("Sending RAG request to Gemini API.")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        logger.info("Successfully received RAG response from Gemini API.")
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error during RAG answer generation: {e}", exc_info=True)
        raise e