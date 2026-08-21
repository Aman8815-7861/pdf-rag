from fastapi import FastAPI

from app.api.routes import router

from core.exception_handlers import (
    pdf_upload_exception_handler,
)

from core.exceptions import (
    PDFUploadError,
)


app = FastAPI(
    title="PDF RAG Assistant",
    version="1.0.0",
    description=(
        "A PDF question-answering system "
        "using Retrieval-Augmented Generation."
    ),
)


app.add_exception_handler(
    PDFUploadError,
    pdf_upload_exception_handler,
)


app.include_router(
    router
)


@app.get("/")
def root():
    return {
        "message": (
            "PDF RAG Assistant is running"
        )
    }