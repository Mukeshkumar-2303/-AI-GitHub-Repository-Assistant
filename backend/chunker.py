from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = []

    for doc in documents:

        split_texts = splitter.split_text(doc["content"])

        for text in split_texts:

            chunks.append({
                "content": text,
                "source": doc["file_path"]
            })

    return chunks