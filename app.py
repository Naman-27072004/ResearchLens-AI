"""
ResearchLens AI - Streamlit Web Application

This file serves as the main entry point for the ResearchLens AI application,
providing a dashboard for uploading, analyzing, searching, comparing, and 
identifying gaps in scientific research papers.

Features:
    - PDF Uploading and Parsing
    - AI-Powered Research Analysis
    - Context-Aware Q&A Chat (RAG)
    - Multi-Paper Comparison
    - Research Gap Detection
    - Citation Analytics
    - Multi-Agent AI Routing (Supervisor-driven)
"""

import os
from dotenv import load_dotenv
load_dotenv()
import logging
import streamlit as st

# Configure logging to write to both stdout and a local file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("researchlens.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

from backend.parser import extract_text_from_pdf
from backend.chunker import split_text
from backend.embeddings import create_embeddings
from backend.vectorstore import create_vector_store
from backend.retriever import retrieve_chunks
from backend.summarizer import analyze_paper
from backend.rag import answer_question
from backend.comparer import compare_papers
from backend.gap_detector import detect_research_gap
from backend.citation_analyzer import citation_analysis
from backend.supervisor import route_query


# ----------------------------------------------------
# ERROR HANDLING HELPER
# ----------------------------------------------------

def handle_api_error(e: Exception, default_msg: str):
    err_str = str(e)
    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
        st.error("⚠️ **Quota Exceeded (Rate Limit or Daily Limit Hit)**:\n\nYou have exceeded the Gemini API Free Tier daily quota (which is strictly limited to 20 requests per day per project/model on the free tier). Please wait for the daily quota to reset, upgrade your plan in Google AI Studio, or try a different Gemini API key.")
    elif "403" in err_str or "PERMISSION_DENIED" in err_str or "API key not valid" in err_str:
        st.error("⚠️ **Invalid API Key or Permission Denied**:\n\nThe Gemini API key provided is not valid or doesn't have permission to access `gemini-2.5-flash`. Please verify the key is typed correctly.")
    elif "API key not found" in err_str or "api_key is required" in err_str:
        st.error("⚠️ **API Key Missing**:\n\nGemini API key was not found. Please paste your key in the sidebar or configure it in your Streamlit secrets.")
    else:
        st.error(f"{default_msg}\n\n*Details: {err_str}*")


# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="ResearchLens AI",
    page_icon="📚",
    layout="wide"
)


st.title("📚 ResearchLens AI")
st.caption("AI-Powered Research Paper Analysis using Gemini + RAG")


# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("📚 ResearchLens")

# Initialize Gemini API Key
api_key = os.environ.get("GEMINI_API_KEY")

# Check Streamlit secrets as fallback
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    os.environ["GEMINI_API_KEY"] = api_key

# Sidebar input for API Key
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 API Configuration")

# Retrieve from session state if already stored
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = api_key or ""

user_api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    value=st.session_state.gemini_api_key,
    help="Enter your Gemini API key. If set via environment variables or Streamlit secrets, it will be pre-filled."
)

if user_api_key:
    st.session_state.gemini_api_key = user_api_key
    os.environ["GEMINI_API_KEY"] = user_api_key

if not os.environ.get("GEMINI_API_KEY"):
    st.sidebar.warning("⚠️ Gemini API key not found. Please enter it above or configure it in your environment / Streamlit secrets.")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### Features

✅ PDF Upload

✅ AI Analysis

✅ Chat with Paper (RAG)

✅ Multi Paper Comparison

✅ Research Gap Detection

✅ Citation Analytics

✅ Multi-Agent AI
""")


# ----------------------------------------------------
# FILE UPLOAD
# ----------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Research Papers",
    type=["pdf"],
    accept_multiple_files=True
)


# ----------------------------------------------------
# SESSION STORAGE
# ----------------------------------------------------

if "papers" not in st.session_state:
    st.session_state.papers = []

if "processed" not in st.session_state:
    st.session_state.processed = False


# ----------------------------------------------------
# PROCESS PAPERS
# ----------------------------------------------------

if uploaded_files:

    if st.button("Process Papers"):

        st.session_state.papers = []

        with st.spinner("Processing research papers..."):

            for uploaded_file in uploaded_files:
                try:
                    logger.info(f"Processing paper: {uploaded_file.name}")
                    text = extract_text_from_pdf(uploaded_file)
                    chunks = split_text(text)
                    embeddings = create_embeddings(chunks)
                    vector_store = create_vector_store(embeddings)

                    paper_data = {
                        "name": uploaded_file.name,
                        "text": text,
                        "chunks": chunks,
                        "embeddings": embeddings,
                        "vector_store": vector_store
                    }

                    st.session_state.papers.append(paper_data)
                except Exception as e:
                    logger.error(f"Error processing paper {uploaded_file.name}: {e}", exc_info=True)
                    st.error(f"Failed to process {uploaded_file.name}: {str(e)}")

        st.session_state.processed = True

        st.success("✅ Research Papers Processed Successfully!")


# ----------------------------------------------------
# AFTER PROCESSING
# ----------------------------------------------------

if st.session_state.processed:

    papers = st.session_state.papers

    # Use first paper for analysis/chat
    paper = papers[0]

    text = paper["text"]
    chunks = paper["chunks"]
    embeddings = paper["embeddings"]
    vector_store = paper["vector_store"]

    # ------------------------------------------------
    # SIDEBAR STATISTICS
    # ------------------------------------------------

    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Statistics")

    st.sidebar.write(f"Number of Papers : {len(papers)}")
    st.sidebar.write(f"Chunks : {len(chunks)}")
    st.sidebar.write(f"Embedding Dimension : {embeddings.shape[1]}")
    st.sidebar.write(f"Vectors Stored : {vector_store.ntotal}")

    # ------------------------------------------------
    # TABS
    # ------------------------------------------------

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📄 Extracted Text",
            "🤖 AI Analysis",
            "💬 Chat",
            "📊 Compare Papers",
            "🔍 Research Gap",
            "📈 Citation Analytics",
            "🤖 Multi-Agent AI",
        ]
    )

    # =================================================
    # TAB 1
    # =================================================

    with tab1:

        st.subheader("Extracted Text")
        st.text_area("Research Paper", text, height=450)

        st.divider()

        st.subheader("Chunk Information")
        st.write(f"Total Chunks : **{len(chunks)}**")

        with st.expander("View First Chunk"):
            st.write(chunks[0])

        st.divider()

        st.subheader("Embedding Information")
        st.write(f"Embedding Shape : **{embeddings.shape}**")

        with st.expander("View First Embedding"):
            st.write(embeddings[0])

        st.divider()

        st.subheader("Vector Store")
        st.success("FAISS Vector Store Created Successfully")
        st.write(f"Vectors Stored : **{vector_store.ntotal}**")

    # =================================================
    # TAB 2
    # =================================================

    with tab2:

        st.subheader("🤖 AI Research Analysis")

        if st.button("Analyze Paper"):
            with st.spinner("Gemini is analyzing..."):
                try:
                    analysis = analyze_paper(text)
                    st.markdown(analysis)
                except Exception as e:
                    logger.error(f"Error during paper analysis: {e}", exc_info=True)
                    handle_api_error(e, "An error occurred while analyzing the paper.")

    # =================================================
    # TAB 3
    # =================================================

    with tab3:

        st.subheader("💬 Chat with Research Paper")

        question = st.text_input("Ask a question about the paper")

        if st.button("Ask AI"):

            if question.strip() == "":
                st.warning("Please enter a question")

            else:
                with st.spinner("Searching paper..."):
                    try:
                        retrieved_chunks = retrieve_chunks(
                            question,
                            vector_store,
                            chunks
                        )
                        answer = answer_question(question, retrieved_chunks)
                        st.success("Answer Generated")
                        st.markdown(answer)
                    except Exception as e:
                        logger.error(f"Error during RAG chat: {e}", exc_info=True)
                        handle_api_error(e, "Failed to retrieve an answer.")

                with st.expander("📚 Retrieved Context"):

                    for i, chunk in enumerate(retrieved_chunks):
                        st.markdown(f"### Chunk {i+1}")
                        st.write(chunk)
                        st.divider()

    # =================================================
    # TAB 4
    # =================================================

    with tab4:

        st.subheader("📊 Multi Paper Comparison")

        if len(papers) < 2:

            st.info("📄 Upload at least 2 research papers for comparison.")

        else:

            st.write(f"Selected Papers: {len(papers)}")

            for p in papers:
                st.write(f"• {p['name']}")

            if st.button("Compare All Papers"):
                with st.spinner("Comparing research papers..."):
                    try:
                        comparison = compare_papers(papers)
                        st.success("✅ Comparison Completed!")
                        st.markdown(comparison)
                    except Exception as e:
                        logger.error(f"Error during paper comparison: {e}", exc_info=True)
                        handle_api_error(e, "Failed to compare papers.")

    # =================================================
    # TAB 5
    # =================================================

    with tab5:

        st.subheader("🔍 Research Gap Detection")

        if len(papers) < 2:

            st.info("Upload at least 2 papers.")

        else:

            if st.button("Detect Research Gap"):
                with st.spinner("Finding research gaps..."):
                    try:
                        gaps = detect_research_gap(papers)
                        st.success("✅ Research Gap Detection Completed!")
                        st.markdown(gaps)
                    except Exception as e:
                        logger.error(f"Error during gap detection: {e}", exc_info=True)
                        handle_api_error(e, "Failed to detect research gaps.")

    # =================================================
    # TAB 6
    # =================================================

    with tab6:

        st.subheader("📈 Citation Analytics")

        try:
            citation_result = citation_analysis(text)
            st.metric("Total References", citation_result["total_references"])
        except Exception as e:
            logger.error(f"Error during citation analysis: {e}", exc_info=True)
            st.error("An error occurred during citation extraction.")
            citation_result = {"total_references": 0, "references": [], "top_authors": []}

        st.divider()

        st.subheader("Top Authors")

        if citation_result["top_authors"]:

            for author, count in citation_result["top_authors"]:
                st.write(f"**{author}** — {count}")

        else:

            st.info("No author information found.")

        st.divider()

        st.subheader("Extracted References")

        if citation_result["references"]:

            for i, ref in enumerate(citation_result["references"], start=1):
                st.write(f"{i}. {ref}")

        else:

            st.warning("No references section found.")

    # =================================================
    # TAB 7
    # =================================================

    with tab7:

        st.subheader("🤖 Multi-Agent AI Assistant")

        user_query = st.text_input(
            "Ask anything about your uploaded research papers"
        )

        if st.button("Run Multi-Agent"):

            if user_query.strip() == "":
                st.warning("Please enter a query.")

            else:

                with st.spinner("Supervisor Agent is selecting the best agent..."):
                    try:
                        agent = route_query(user_query)
                        st.success(f"Supervisor selected: {agent}")

                        if agent == "summary":
                            result = analyze_paper(text)
                        elif agent == "comparison":
                            result = compare_papers(papers)
                        elif agent == "research_gap":
                            result = detect_research_gap(papers)
                        elif agent == "citation":
                            agent_citation = citation_analysis(text)
                            result = f"### Citation Analytics\n\nTotal References: {agent_citation['total_references']}\n\nTop Authors:\n\n{agent_citation['top_authors']}"
                        else:
                            retrieved_chunks = retrieve_chunks(user_query, vector_store, chunks)
                            result = answer_question(user_query, retrieved_chunks)

                        st.markdown(result)
                    except Exception as e:
                        logger.error(f"Error in Multi-Agent run: {e}", exc_info=True)
                        handle_api_error(e, "Multi-Agent run failed.")

else:
    st.info("👆 Upload Research Paper PDF to begin.")