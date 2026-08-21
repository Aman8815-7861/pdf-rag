from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import (
    HuggingFaceEmbeddings,
)


class RAGRepository:
    """
    Repository responsible for interacting
    with the local Chroma vector store.
    """

    def __init__(
        self,
        embedding_model: HuggingFaceEmbeddings,
        persist_directory: str,
        collection_name: str = "pdf_rag",
    ):
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=persist_directory,
        )

    def add_documents(
        self,
        documents: list[Document],
    ) -> None:
        """
        Store document chunks in Chroma.
        """

        if not documents:
            raise ValueError(
                "No documents were provided."
            )

        self.vector_store.add_documents(
            documents
        )

    def get_retriever(
        self,
        k: int = 4,
    ):
        """
        Return a similarity-based retriever.
        """

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": k,
            },
        )