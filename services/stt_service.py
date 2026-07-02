"""STT service — Mistral Voxtral offline transcription.

Drop-in replacement for stt_service.transcribe().
Accepts WebM/Opus bytes from streamlit-mic-recorder directly.
"""

from mistralai import Mistral

from config import MISTRAL_API_KEY

_client = Mistral(api_key=MISTRAL_API_KEY)


def transcribe(audio_bytes: bytes, language: str | None = None) -> str:
    """Transcribe audio bytes using Mistral voxtral-mini-latest.

    Args:
        audio_bytes: Raw audio from mic_recorder (WebM/Opus) or any format
                     Mistral accepts (mp3, wav, webm, ogg, flac, m4a).
        language:    BCP-47 code (e.g. "en", "fr"). None = auto-detect.

    Returns:
        Transcribed text, or "" on empty/unrecognised audio.
    """
    kwargs = dict(
        model="voxtral-mini-latest",
        file={"content": audio_bytes, "file_name": "audio.webm"},
    )
    if language:
        kwargs["language"] = language

    response = _client.audio.transcriptions.complete(**kwargs)
    return (response.text or "").strip()
