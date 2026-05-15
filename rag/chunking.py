from langchain.text_splitter import RecursiveCharacterTextSplitter


def crear_chunks(
    texto,
    chunk_size=1000,
    chunk_overlap=200
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return splitter.split_text(texto)