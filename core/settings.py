import os

from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Please add GROQ_API_KEY to your .env file."
    )


PDF_DIRECTORY = "data/pdfs"

VECTOR_STORE_DIRECTORY = "data/vector_store"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

RETRIEVER_K = 4

LLM_MODEL = "openai/gpt-oss-120b"

LLM_TEMPERATURE = 0