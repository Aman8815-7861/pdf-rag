from langchain_core.output_parsers import (
    StrOutputParser,
)
from langchain_core.prompts import (
    ChatPromptTemplate,
)


class RAGService:
    """
    Service responsible for the complete
    Retrieval-Augmented Generation process.
    """

    def __init__(
        self,
        retriever,
        llm,
    ):
        self.retriever = retriever

        self.llm = llm

        self.prompt = (
            ChatPromptTemplate.from_template(
                """
You are a helpful assistant that answers
questions using the provided PDF context.

Rules:

1. Answer the question using only the
   provided context.

2. Do not make up information.

3. If the answer cannot be found in the
   provided context, clearly say that the
   information is not available in the
   provided document.

4. Give a clear and concise answer.

Context:
{context}

Question:
{question}

Answer:
"""
            )
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(
        self,
        question: str,
    ) -> dict:
        """
        Retrieve relevant chunks and generate
        an answer using the language model.
        """

        documents = (
            self.retriever.invoke(
                question
            )
        )

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        answer = self.chain.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        sources = []

        for document in documents:
            source = document.metadata.get(
                "source"
            )

            page = document.metadata.get(
                "page",
                0,
            )

            sources.append(
                {
                    "source": source,
                    "page": page + 1,
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }