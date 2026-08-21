from langchain_groq import ChatGroq

from core.settings import (
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
)


class LLMService:
    """
    Service responsible for configuring
    and providing the language model.
    """

    def __init__(
        self,
        model: str = LLM_MODEL,
        temperature: float = LLM_TEMPERATURE,
    ):
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            api_key=GROQ_API_KEY,
        )

    def get_llm(self) -> ChatGroq:
        """
        Return the configured language model.
        """

        return self.llm