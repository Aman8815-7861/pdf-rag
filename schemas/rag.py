from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    Request body for asking a question.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the uploaded PDF.",
    )


class SourceResponse(BaseModel):
    """
    Information about the PDF source
    used to generate the answer.
    """

    source: str | None = None

    page: int


class QuestionResponse(BaseModel):
    """
    Response returned by the RAG system.
    """

    answer: str

    sources: list[SourceResponse]