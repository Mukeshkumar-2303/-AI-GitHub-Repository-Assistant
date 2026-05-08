**AI-Powered GitHub Repository Knowledge Assistant

An intelligent Retrieval-Augmented Generation (RAG) system that allows users to understand any GitHub repository using natural language queries.

It analyzes real repository code (not just README) and provides grounded, evidence-based answers.

Features
Input any public GitHub repository URL
Auto-clone repository locally
Extract and analyze real source code files
Intelligent code chunking (function/class level)
Embedding-based semantic search
Vector database storage (FAISS / ChromaDB)
LLM-powered Q&A (Groq / OpenAI / Ollama)
Accurate file structure visualization
Anti-hallucination system (answers only from code)
Retrieval transparency with source tracking
How It Works
GitHub URL
   ↓
Clone Repository
   ↓
Parse Source Files
   ↓
Chunk Code (functions/classes)
   ↓
Generate Embeddings
   ↓
Store in Vector DB
   ↓
User Question
   ↓
Retrieve Relevant Chunks
   ↓
LLM Generates Answer (Grounded in Code)
Supported File Types
.py
.js
.ts
.java
.md
.json
.yaml
.sql
.html
.css
Ignored Files and Folders
node_modules
.git
pycache
venv
build
dist
Requirements
Repository must be a public GitHub repository
Must contain source code files
README alone is not sufficient
Large repositories may take time to process
Tech Stack

Frontend:

Streamlit

Backend:

Python

AI / LLM:

LangChain
Groq / OpenAI / Ollama

Embeddings:

HuggingFace Transformers
Sentence Transformers
CodeBERT (optional)

Vector Database:

FAISS / ChromaDB

Repository Handling:

GitPython
Key Capabilities
Repository Understanding
Project explanation
Architecture overview
Tech stack detection
Dependency analysis
Code Analysis
Function explanation
Class-level breakdown
API flow tracking
Smart Q&A
Context-aware answers
File-specific queries
Implementation tracing
Example Queries
General Understanding
What is this project about?
Explain this repository in simple terms.
File Structure
Show file structure of this repository
List all files in this project
Code Understanding
How does the backend work?
Explain the main logic of this project
Deep Analysis
Which file handles embeddings?
Where is vector database created?
How is repository cloned?
Advanced Features (Future Scope)
GitHub Copilot-style UI
Clickable file explorer
Code viewer with syntax highlighting
Chat per file
Architecture diagram generation
Multi-repository support
CI/CD integration
Limitations
Large repositories may take time to index
Complex distributed systems may not be fully interpreted
Requires well-structured repositories for best performance
Output Principle

The system answers ONLY using retrieved repository context.
If information is not found in the repository, it explicitly states that.

Author

Built as an AI-powered RAG system for:

Code understanding
Repository exploration
Developer productivity
Future Improvements
Faster indexing with parallel processing
Real-time GitHub sync
Multi-language model routing
UI-based file explorer tree
Code execution sandbox integration
