"""
FastAPI backend for the HR Chatbot.

Endpoints:
- GET  /       → Health check
- POST /upload → Upload and index a PDF
- POST /chat   → Ask a question against the indexed PDF
"""

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chatbot import generate_answer
from chunking import split_text_into_chunks
from config import load_api_key
from pdf_loader import extract_text_from_pdf
from vectordb import index_chunks, is_document_indexed, search_similar_chunks

app = FastAPI(
    title="HR Chatbot API",
    description="Upload an HR PDF and ask questions using RAG + Gemini.",
    version="1.0.0",
)

# Allow frontend (local HTML/JS) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question about the PDF")


class ChatResponse(BaseModel):
    answer: str
    sources_used: int


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int


@app.on_event("startup")
def validate_config() -> None:
    """Fail fast if API key is missing when server starts."""
    try:
        load_api_key()
    except ValueError as exc:
        raise RuntimeError(str(exc)) from exc


@app.get("/")
def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {
        "status": "ok",
        "message": "HR Chatbot backend is running",
        "document_indexed": str(is_document_indexed()).lower(),
    }


@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload a PDF, extract text, chunk it, embed, and store in ChromaDB.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        text = extract_text_from_pdf(file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {exc}") from exc

    try:
        chunks = split_text_into_chunks(text)
        chunk_count = index_chunks(chunks, source_filename=file.filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to index document: {exc}") from exc

    return UploadResponse(
        message="PDF uploaded and indexed successfully.",
        filename=file.filename,
        chunks_created=chunk_count,
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Accept a question, retrieve top 3 chunks, and ask Gemini for an answer.
    """
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if not is_document_indexed():
        raise HTTPException(
            status_code=400,
            detail="No PDF uploaded yet. Please upload a document before asking questions.",
        )

    try:
        context_chunks = search_similar_chunks(question, top_k=3)
        answer = generate_answer(context_chunks, question)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chat failed: {exc}") from exc

    return ChatResponse(answer=answer, sources_used=len(context_chunks))
