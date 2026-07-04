"""
Store and search document chunks in a local ChromaDB vector database.
Uses the native ChromaDB client (works on Windows without C++ build tools).
"""

import chromadb

from config import CHROMA_DIR, COLLECTION_NAME
from embedding import embed_query, embed_texts

# Module-level flag: has a PDF been uploaded and indexed?
_document_indexed: bool = False


def _get_client() -> chromadb.PersistentClient:
    """Return a persistent local ChromaDB client."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def _get_collection():
    """Get or create the document collection."""
    client = _get_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def index_chunks(chunks: list[str], source_filename: str) -> int:
    """
    Store text chunks in ChromaDB (replaces previous document).

    Returns the number of chunks stored.
    """
    global _document_indexed

    client = _get_client()

    # Remove old collection and create a fresh one
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    embeddings = embed_texts(chunks)
    metadatas = [{"source": source_filename, "chunk_index": i} for i in range(len(chunks))]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    _document_indexed = True
    return len(chunks)


def is_document_indexed() -> bool:
    """Check whether a document has been uploaded and indexed."""
    global _document_indexed

    if _document_indexed:
        return True

    if not CHROMA_DIR.exists():
        return False

    try:
        collection = _get_collection()
        count = collection.count()
        _document_indexed = count > 0
        return _document_indexed
    except Exception:
        return False


def search_similar_chunks(query: str, top_k: int = 3) -> list[str]:
    """
    Perform semantic search and return the top matching chunk texts.

    Uses cosine similarity via ChromaDB + Gemini embeddings.
    """
    if not is_document_indexed():
        raise ValueError("No PDF has been uploaded yet. Please upload a document first.")

    collection = _get_collection()
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents"],
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        raise ValueError("No relevant information found in the uploaded document.")

    return documents
