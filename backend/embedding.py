"""
Create text embeddings using Google's Gemini embedding model via LangChain.
"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import load_api_key

# Current Gemini embedding model (text-embedding-004 is deprecated)
EMBEDDING_MODEL = "models/gemini-embedding-001"


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """Return a configured Gemini embeddings client."""
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=load_api_key(),
    )


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert a list of text chunks into embedding vectors."""
    embeddings = get_embedding_model()
    return embeddings.embed_documents(texts)


def embed_query(query: str) -> list[float]:
    """Convert a user question into a single embedding vector."""
    embeddings = get_embedding_model()
    return embeddings.embed_query(query)
