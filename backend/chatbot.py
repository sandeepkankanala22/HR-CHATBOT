"""
Send retrieved context and user question to Gemini for the final answer.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import load_api_key

# Gemini chat model for generating answers
CHAT_MODEL = "gemini-2.5-flash"


def build_context_prompt(context_chunks: list[str], question: str) -> str:
    """Format retrieved chunks into a prompt for Gemini."""
    context_block = "\n\n---\n\n".join(
        f"Chunk {i + 1}:\n{chunk}" for i, chunk in enumerate(context_chunks)
    )

    return (
        "Use ONLY the context below to answer the user's HR-related question.\n"
        "If the answer is not in the context, say: "
        "'I could not find that information in the uploaded document.'\n\n"
        f"CONTEXT:\n{context_block}\n\n"
        f"QUESTION:\n{question}"
    )


def generate_answer(context_chunks: list[str], question: str) -> str:
    """
    Call Gemini with retrieved chunks + question and return the answer.

    Why not send the whole PDF?
    - Token limits, cost, latency, and better accuracy with focused context.
    """
    llm = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        google_api_key=load_api_key(),
        temperature=0.2,
    )

    system_message = SystemMessage(
        content=(
            "You are a helpful HR assistant. Answer clearly and concisely "
            "based only on the provided document context. Do not invent policies."
        )
    )

    user_message = HumanMessage(content=build_context_prompt(context_chunks, question))

    try:
        response = llm.invoke([system_message, user_message])
    except Exception as exc:
        raise RuntimeError(f"Gemini is unavailable: {exc}") from exc

    answer = response.content if hasattr(response, "content") else str(response)

    if not answer or not str(answer).strip():
        raise ValueError("Gemini returned an empty answer.")

    return str(answer).strip()
