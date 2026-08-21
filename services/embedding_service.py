from langchain_huggingface import (
    HuggingFaceEmbeddings,
)


class EmbeddingService:
    """
    Service responsible for generating
    embeddings for document chunks.
    """

    def __init__(
        self,
        model_name: str = (
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        ),
    ):
        self.embeddings = (
            HuggingFaceEmbeddings(
                model_name=model_name,
            )
        )

    def get_embeddings(
        self,
    ) -> HuggingFaceEmbeddings:
        """
        Return the configured embedding model.
        """

        return self.embeddings