from pathlib import Path

from core.exceptions import (
    EmptyFileError,
    FileNotProvidedError,
    InvalidFileTypeError,
)

from services.pdf_service import PDFService

from services.chunking_service import (
    ChunkingService,
)

from repositories.rag_repository import (
    RAGRepository,
)


class UploadService:
    """
    Service responsible for validating,
    saving, and indexing uploaded PDFs.
    """

    def __init__(
        self,
        pdf_service: PDFService,
        chunking_service: ChunkingService,
        rag_repository: RAGRepository,
    ):
        self.pdf_service = pdf_service

        self.chunking_service = (
            chunking_service
        )

        self.rag_repository = (
            rag_repository
        )

    def upload(
        self,
        file_path: Path,
        file_content: bytes,
    ) -> int:
        """
        Validate, save, process, and index
        the uploaded PDF.

        Returns:
            Number of chunks created.
        """

        if not file_path.name:
            raise FileNotProvidedError()

        if file_path.suffix.lower() != ".pdf":
            raise InvalidFileTypeError()

        if not file_content:
            raise EmptyFileError()

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_bytes(
            file_content
        )

        documents = (
            self.pdf_service.load_pdf(
                str(file_path)
            )
        )

        chunks = (
            self.chunking_service
            .split_documents(
                documents
            )
        )

        self.rag_repository.add_documents(
            chunks
        )

        return len(chunks)