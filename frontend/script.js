/**
 * HR Chatbot frontend
 * Talks to FastAPI backend at http://127.0.0.1:8000
 */

const API_BASE = "http://127.0.0.1:8080";

const pdfInput = document.getElementById("pdfInput");
const uploadBtn = document.getElementById("uploadBtn");
const uploadStatus = document.getElementById("uploadStatus");
const chatHistory = document.getElementById("chatHistory");
const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");

let documentReady = false;

function setStatus(message, type = "") {
  uploadStatus.textContent = message;
  uploadStatus.className = `status ${type}`.trim();
}

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;

  const label = role === "user" ? "You" : "Assistant";
  div.innerHTML = `<strong>${label}:</strong><span></span>`;
  div.querySelector("span").textContent = text;

  chatHistory.appendChild(div);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function uploadPdf() {
  const file = pdfInput.files[0];

  if (!file) {
    setStatus("Please choose a PDF file first.", "error");
    return;
  }

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    setStatus("Invalid file type. Please upload a PDF.", "error");
    return;
  }

  uploadBtn.disabled = true;
  setStatus("Uploading and indexing PDF...");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Upload failed.");
    }

    documentReady = true;
    setStatus(
      `${data.message} (${data.chunks_created} chunks created from "${data.filename}")`,
      "success"
    );
    addMessage("bot", "Document ready. You can now ask questions about it.");
  } catch (error) {
    documentReady = false;
    setStatus(error.message, "error");
  } finally {
    uploadBtn.disabled = false;
  }
}

async function askQuestion() {
  const question = questionInput.value.trim();

  if (!question) {
    addMessage("bot", "Please enter a question first.");
    return;
  }

  if (!documentReady) {
    addMessage("bot", "Please upload a PDF before asking questions.");
    return;
  }

  addMessage("user", question);
  questionInput.value = "";
  askBtn.disabled = true;

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Could not get an answer.");
    }

    addMessage("bot", data.answer);
  } catch (error) {
    addMessage("bot", error.message);
  } finally {
    askBtn.disabled = false;
    questionInput.focus();
  }
}

uploadBtn.addEventListener("click", uploadPdf);
askBtn.addEventListener("click", askQuestion);

questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    askQuestion();
  }
});

// Optional: check backend health on page load
fetch(`${API_BASE}/`)
  .then((res) => res.json())
  .then((data) => {
    if (data.document_indexed === "true") {
      documentReady = true;
      setStatus("A document is already indexed. You can ask questions.", "success");
    }
  })
  .catch(() => {
    setStatus("Backend not reachable. Start the FastAPI server first.", "error");
  });
