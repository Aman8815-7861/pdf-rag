from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFService:
    """
    Service responsible for loading PDF files.
    """

    def load_pdf(
        self,
        file_path: str,
    ) -> list[Document]:
        """
        Load a PDF and convert each page
        into a LangChain Document.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a PDF file, "
                f"but received: {path.suffix}"
            )

        loader = PyPDFLoader(
            str(path)
        )

        documents = loader.load()

        return documents