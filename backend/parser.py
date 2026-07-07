"""
PDF Parser Module

This module handles extracting raw text from uploaded PDF research papers using
the PyMuPDF (fitz) library.
"""

import logging
from typing import Any
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file: Any) -> str:
    """
    Extracts all text content from a PDF file stream.

    Args:
        pdf_file (BytesIO): A file-like object containing the PDF content.

    Returns:
        str: The full text extracted from the PDF pages.
    """
    logger.info("Opening PDF file stream for text extraction.")
    text = ""
    try:
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        pdf.close()
        logger.info(f"Successfully extracted {len(text)} characters of text from PDF.")
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}", exc_info=True)
        raise RuntimeError(f"Error parsing PDF: {str(e)}")