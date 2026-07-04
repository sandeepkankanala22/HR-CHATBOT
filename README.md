# HR Chatbot

A beginner-friendly **AI-powered HR Chatbot** that lets you upload a PDF (HR policy, handbook, resume, etc.) and ask questions about it using **RAG (Retrieval-Augmented Generation)**.

## What This Project Does

1. Upload a PDF through a simple web page
2. Extract text from the PDF
3. Split text into chunks
4. Create embeddings with **Google Gemini**
5. Store embeddings in **ChromaDB** (local vector database)
6. When you ask a question, perform **semantic search**
7. Send only the top 3 relevant chunks to **Gemini**
8. Display Gemini's answer in the chat UI

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python, FastAPI |
| AI | Google Gemini (embeddings + chat) |
| Vector DB | ChromaDB |
| Libraries | LangChain, PyPDF, python-dotenv |

## Project Structure

```
HR Chatbot/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── vectordb.py
│   ├── chatbot.py
│   └── requirements.txt
├── .env/
│   └── keys          ← Your Gemini API key (not committed to Git)
├── chroma_db/        ← Auto-created vector storage
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.10 or higher
- A Google Gemini API key
- A modern web browser

## Installation

### 1. Open the project folder

```bash
cd "HR Chatbot"
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure your API key

Your key should be stored at:

```
.env/keys
```

Supported formats:

```env
GEMINI_API_KEY=your_key_here
```

or

```env
key=your_key_here
```

**Never commit your API key to GitHub.**

## Run the Application

### Step 1 — Start the backend

From the project root:

```bash
cd backend
uvicorn main:app --reload --port 8080
```

Backend runs at: **http://127.0.0.1:8080**

Health check: **http://127.0.0.1:8080/**

API docs: **http://127.0.0.1:8080/docs**

### Step 2 — Open the frontend

Option A — Open the file directly:

- Double-click `frontend/index.html`

Option B — Use a simple local server (recommended):

```bash
cd frontend
python -m http.server 5500
```

Then open: **http://127.0.0.1:5500**

## How to Test

1. Start the backend
2. Open the frontend
3. Upload a PDF (HR policy or handbook works best)
4. Wait for: `PDF uploaded and indexed successfully`
5. Ask a question, for example:
   - `What is the leave policy?`
   - `How many sick days are allowed?`
6. Read the answer in the chat area

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/upload` | POST | Upload and index a PDF |
| `/chat` | POST | Ask a question about the uploaded PDF |

### Example: Chat request

```json
POST /chat
{
  "question": "What is the probation period?"
}
```

## Project Flow

```
Upload PDF
    ↓
Extract Text (PyPDF)
    ↓
Chunk Text (RecursiveCharacterTextSplitter)
    ↓
Create Embeddings (Gemini)
    ↓
Store in ChromaDB
    ↓
User asks question
    ↓
Convert question to embedding
    ↓
Semantic search → Top 3 chunks
    ↓
Send context + question to Gemini
    ↓
Return answer to frontend
```

## Key Concepts (Interview Prep)

### RAG
Retrieve relevant document chunks first, then generate an answer with an LLM.

### Embeddings
Numbers that represent meaning. Similar text → similar vectors.

### Semantic Search
Finds content by meaning, not just exact keywords.

### ChromaDB
A vector database optimized for similarity search.

## Error Handling

The app handles:

- No PDF uploaded
- Empty or invalid PDF
- Missing API key
- Empty questions
- Gemini unavailable
- No relevant chunks found

## Future Improvements

- Support multiple PDF uploads
- Show source chunk citations in answers
- User authentication
- Chat session memory
- Deploy to cloud (Render, Railway, AWS)
- Better UI with streaming responses
- OCR for scanned PDFs

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend not reachable | Run `uvicorn main:app --reload --port 8080` from `backend/` |
| API key error | Check `.env/keys` format |
| Empty PDF error | Use a text-based PDF, not a scanned image |
| CORS issues | Use `python -m http.server` for frontend |

## License

Educational project for learning AI development.
