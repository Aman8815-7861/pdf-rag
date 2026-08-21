from fastapi import Request
from fastapi.responses import JSONResponse

from core.exceptions import PDFUploadError


async def pdf_upload_exception_handler(
    request: Request,
    exc: PDFUploadError,
):
    """
    Convert PDF upload exceptions
    into HTTP responses.
    """

    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message
        },
    )