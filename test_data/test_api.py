"""Local end-to-end API test for HR Chatbot."""

import json
from pathlib import Path

import requests

BASE = "http://127.0.0.1:8080"
PDF = Path(__file__).resolve().parent / "sample_hr_policy.pdf"


def main() -> None:
    health = requests.get(f"{BASE}/", timeout=30)
    print("HEALTH", health.status_code, health.json())

    with PDF.open("rb") as pdf_file:
        upload = requests.post(
            f"{BASE}/upload",
            files={"file": ("sample_hr_policy.pdf", pdf_file, "application/pdf")},
            timeout=120,
        )
    print("UPLOAD", upload.status_code, upload.text)

    chat = requests.post(
        f"{BASE}/chat",
        json={"question": "How many annual leave days do employees get?"},
        timeout=120,
    )
    print("CHAT", chat.status_code, chat.text)


if __name__ == "__main__":
    main()


# this a just a comment