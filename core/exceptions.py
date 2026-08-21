class PDFUploadError(Exception):
    """
    Base exception for PDF upload-related errors.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class FileNotProvidedError(PDFUploadError):
    """
    Raised when no file is provided.
    """

    def __init__(self):
        super().__init__(
            "No file was provided."
        )


class InvalidFileTypeError(PDFUploadError):
    """
    Raised when the uploaded file is not a PDF.
    """

    def __init__(self):
        super().__init__(
            "Only PDF files are allowed."
        )


class EmptyFileError(PDFUploadError):
    """
    Raised when the uploaded file is empty.
    """

    def __init__(self):
        super().__init__(
            "The uploaded PDF is empty."
        )