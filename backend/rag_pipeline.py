from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from backend.prompt_template import RAG_PROMPT


def create_rag_chain(vector_db):

    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    prompt = PromptTemplate(
        template=RAG_PROMPT,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    return qa_chain