import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def answer_question(question, retrieved_chunks):

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

    response = model.generate_content(prompt)

    return response.text