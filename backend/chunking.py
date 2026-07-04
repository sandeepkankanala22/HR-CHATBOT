"""
Split long document text into smaller overlapping chunks for embedding.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Chunk size: characters per piece (not tokens)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def split_text_into_chunks(text: str) -> list[str]:
    """
    Split document text using RecursiveCharacterTextSplitter.

    Why chunking?
    - LLMs and embedding models work better on smaller passages.
    - Semantic search returns precise relevant sections, not whole documents.

    Why overlap?
    - Prevents sentences/ideas from being cut in half at chunk boundaries.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_text(text)

    if not chunks:
        raise ValueError("Text chunking produced no chunks.")

    return chunks
