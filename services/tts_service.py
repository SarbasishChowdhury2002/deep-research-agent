"""TTS service — Mistral Voxtral via direct HTTP API."""

import base64
import re

import requests

from config import MISTRAL_API_KEY, VOXTRAL_VOICE

MODEL_ID = "voxtral-mini-tts-2603"
_API_URL = "https://api.mistral.ai/v1/audio/speech"


def _strip_markdown(text: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)   # headers
    text = re.sub(r"[*_`~]+", "", text)                           # emphasis/code
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)  # bullets
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)         # links → text
    return text.strip()


def synthesise(text: str) -> bytes:
    """Synthesise plain text to MP3 bytes."""
    response = requests.post(
        _API_URL,
        headers={
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL_ID,
            "input": text,
            "voice_id": VOXTRAL_VOICE,
            "response_format": "mp3",
        },
        timeout=60,
    )
    response.raise_for_status()
    return base64.b64decode(response.json()["audio_data"])


def synthesise_report(text: str) -> bytes:
    """Strip markdown from *text* then synthesise to MP3 bytes.

    Use this when the input may contain markdown (e.g. a research report).
    """
    return synthesise(_strip_markdown(text))
