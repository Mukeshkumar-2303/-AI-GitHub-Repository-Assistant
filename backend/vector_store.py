from langchain_community.vectorstores import FAISS
from langchain.schema import Document


def create_vector_store(chunks, embeddings):

    docs = []

    for chunk in chunks:

        docs.append(
            Document(
                page_content=chunk["content"],
                metadata={
                    "source": chunk["source"]
                }
            )
        )

    vector_db = FAISS.from_documents(docs, embeddings)

    return vector_db