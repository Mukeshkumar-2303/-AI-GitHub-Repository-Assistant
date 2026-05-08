import streamlit as st
import re
from dotenv import load_dotenv

from backend.github_handler import clone_repository
from backend.parser import load_repository_files, get_file_structure
from backend.chunker import chunk_documents
from backend.embeddings import load_embedding_model
from backend.vector_store import create_vector_store
from backend.rag_pipeline import create_rag_chain

load_dotenv()

# PAGE CONFIG
st.set_page_config(
    page_title="GitHub Repository Assistant",
    layout="wide"
)

st.title("AI-Powered GitHub Repository Assistant")

# HERO INFO
st.info("""
💡 How this AI Works:

1. Enter a GitHub repository URL
2. System clones real repository code
3. Only supported files are processed
4. Code is chunked intelligently
5. AI retrieves relevant code only
6. Answers are grounded in real repository
""")

# SIDEBAR RULES
st.sidebar.title("Repository Rules")

st.sidebar.subheader("Supported Files")
st.sidebar.write([
    ".py", ".js", ".ts", ".java",
    ".md", ".json", ".yaml", ".sql",
    ".html", ".css"
])

st.sidebar.subheader("Ignored Folders")
st.sidebar.write([
    "node_modules", ".git", "__pycache__",
    "venv", "build", "dist"
])

st.sidebar.subheader("Requirements")
st.sidebar.write("""
- Public GitHub repo only
- Must contain source code
- README alone is not enough
- Large repos take time
""")

# SESSION STATE INIT
for key in ["docs", "chunks", "qa_chain", "file_structure"]:
    if key not in st.session_state:
        st.session_state[key] = None

# RESET SESSION
if st.button("Reset Session"):
    st.session_state.docs = None
    st.session_state.chunks = None
    st.session_state.qa_chain = None
    st.session_state.file_structure = None
    st.success("Session reset successfully.")

# INPUT
repo_url = st.text_input("Enter GitHub Repository URL")
repo_path = None

# INGESTION PIPELINE
if st.button("Analyze Repository"):

    if not repo_url:
        st.error("Please enter a valid GitHub repository URL")
        st.stop()

    pattern = r"^https://github\.com/[\w.-]+/[\w.-]+/?$"

    if not re.match(pattern, repo_url):
        st.error("❌ Invalid GitHub repository URL")
        st.stop()

    # Clone repo
    with st.spinner("Cloning repository..."):
        repo_path, error = clone_repository(repo_url)

    if error:
        st.error(error)
        st.stop()

    st.success("Repository cloned successfully.")

    # FILE STRUCTURE
    st.session_state.file_structure = get_file_structure(repo_path)

    st.subheader("Repository Structure")
    for file in st.session_state.file_structure:
        clean_path = file.split("repositories")[-1]
        clean_path = clean_path.replace("\\", "/").strip("/")
        st.write(clean_path)

    # PARSE FILES
    with st.spinner("Parsing repository files..."):
        docs = load_repository_files(repo_path)

    if not docs:
        st.error("No supported source files found in repository.")
        st.stop()

    st.session_state.docs = docs

    st.write("📄 Total files found:", len(docs))
    st.write("📌 Sample file:", docs[0])

    # CHUNKING
    with st.spinner("Chunking documents..."):
        chunks = chunk_documents(docs)

    if not chunks:
        st.error("No valid chunks generated.")
        st.stop()

    st.session_state.chunks = chunks

    st.write("✂️ Total chunks created:", len(chunks))
    st.write("📌 Sample chunk:", chunks[0])

    # EMBEDDINGS + VECTOR DB
    with st.spinner("Generating embeddings..."):
        embeddings = load_embedding_model()
        vector_db = create_vector_store(chunks, embeddings)

    st.success("Repository indexed successfully.")

    qa_chain = create_rag_chain(vector_db)
    st.session_state.qa_chain = qa_chain

# QA SECTION
if st.session_state.qa_chain:

    st.divider()

    question = st.text_input("Ask Questions About Repository")

    # FILE STRUCTURE QUICK HANDLER
    if question and any(x in question.lower() for x in [
        "file structure", "list files", "project structure"
    ]):
        st.subheader("File Structure")
        for file in st.session_state.file_structure:
            clean_path = file.split("repositories")[-1]
            clean_path = clean_path.replace("\\", "/").strip("/")
            st.write("📄", clean_path)
        st.stop()

    # ASK RAG
    if st.button("Ask"):

        if not question:
            st.error("Please enter a question")
            st.stop()

        with st.spinner("Generating answer..."):
            result = st.session_state.qa_chain.invoke(
                {"query": question}
            )

        # ANSWER
        st.subheader("Answer")
        st.write(result["result"])

        # SOURCES
        st.subheader("Sources")
        sources = set()

        for doc in result.get("source_documents", []):
            sources.add(doc.metadata.get("source", "Unknown"))

        for src in sources:
            st.code(src)

        # RETRIEVAL DEBUG
        st.divider()
        st.subheader("Retrieval Debug")

        if result.get("source_documents"):
            for i, doc in enumerate(result["source_documents"]):
                st.markdown(f"### Chunk {i+1}")
                st.code(doc.metadata.get("source", "Unknown"))
                st.text(doc.page_content[:500])
        else:
            st.warning("No source documents retrieved.")

        # DEBUG INFO
        st.divider()
        st.subheader("Debug Info")

        st.write("Total Documents:", len(st.session_state.docs or []))
        st.write("Total Chunks:", len(st.session_state.chunks or []))
