from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    UploadFile,
)

from core.settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    PDF_DIRECTORY,
    RETRIEVER_K,
    VECTOR_STORE_DIRECTORY,
)

from repositories.rag_repository import (
    RAGRepository,
)

from schemas.rag import (
    QuestionRequest,
    QuestionResponse,
)

from services.chunking_service import (
    ChunkingService,
)

from services.embedding_service import (
    EmbeddingService,
)

from services.llm_service import (
    LLMService,
)

from services.pdf_service import (
    PDFService,
)

from services.rag_service import (
    RAGService,
)

from services.upload_service import (
    UploadService,
)


router = APIRouter(
    prefix="/api/v1/rag",
    tags=["RAG"],
)


# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

DATA_DIRECTORY = Path(
    PDF_DIRECTORY
)

DATA_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# Services and Repository
# ---------------------------------------------------------

embedding_service = (
    EmbeddingService()
)


rag_repository = RAGRepository(
    embedding_model=(
        embedding_service.get_embeddings()
    ),
    persist_directory=(
        VECTOR_STORE_DIRECTORY
    ),
)


pdf_service = PDFService()


chunking_service = ChunkingService(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


upload_service = UploadService(
    pdf_service=pdf_service,
    chunking_service=chunking_service,
    rag_repository=rag_repository,
)


llm_service = LLMService()


rag_service = RAGService(
    retriever=(
        rag_repository.get_retriever(
            k=RETRIEVER_K
        )
    ),
    llm=llm_service.get_llm(),
)


# ---------------------------------------------------------
# Upload PDF
# ---------------------------------------------------------

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
):
    """
    Upload a PDF, process it, create chunks,
    generate embeddings, and store them in Chroma.
    """

    filename = Path(
        file.filename or ""
    ).name

    file_path = (
        DATA_DIRECTORY / filename
    )

    file_content = await file.read()

    number_of_chunks = (
        upload_service.upload(
            file_path=file_path,
            file_content=file_content,
        )
    )

    return {
        "message": (
            "PDF uploaded and indexed "
            "successfully."
        ),
        "filename": filename,
        "chunks": number_of_chunks,
    }


# ---------------------------------------------------------
# Ask Question
# ---------------------------------------------------------

@router.post(
    "/ask",
    response_model=QuestionResponse,
)
async def ask_question(
    request: QuestionRequest,
):
    """
    Ask a question about the uploaded PDFs.
    """

    result = rag_service.ask(
        question=request.question,
    )

    return result