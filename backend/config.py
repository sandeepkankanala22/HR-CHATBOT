"""
Load configuration and secrets from the project .env/keys file.
"""

from pathlib import Path

from dotenv import load_dotenv
import os


# Project root is one level above backend/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KEYS_FILE = PROJECT_ROOT / ".env" / "keys"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "hr_documents"

# Alternate key names we accept in the keys file
_KEY_NAMES = {"key", "gemini_api_key", "api_key", "google_api_key"}


def _parse_keys_file() -> str | None:
    """Parse key=value lines from .env/keys without printing secrets."""
    if not KEYS_FILE.exists():
        return None

    content = KEYS_FILE.read_text(encoding="utf-8-sig").strip()
    if not content:
        return None

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        name, value = line.split("=", 1)
        if name.strip().lower() in _KEY_NAMES and value.strip():
            return value.strip()

    return None


def load_api_key() -> str:
    """
    Load Gemini API key from .env/keys or environment variable.

    Supported .env/keys formats:
    - key=your_api_key
    - GEMINI_API_KEY=your_api_key
    """
    load_dotenv(KEYS_FILE)

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("key") or _parse_keys_file()

    if not api_key:
        raise ValueError(
            f"Gemini API key not found. Save your key in: {KEYS_FILE}\n"
            "Example format:\n"
            "key=your_gemini_api_key_here"
        )

    return api_key
