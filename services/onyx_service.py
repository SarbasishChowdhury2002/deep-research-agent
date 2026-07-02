"""Onyx Cloud document ingestion client."""

from pathlib import Path

import requests
from config import ONYX_BASE_URL, ONYX_HEADERS, ONYX_CC_PAIR_ID


def ingest_document(filename: str, text: str, session_id: str) -> bool:
    """Index a document in Onyx Cloud. Returns True on success."""
    normalized_name = Path(filename).name
    file_ext = Path(normalized_name).suffix.lower()

    payload = {
        "document": {
            # Stable identifier ensures re-ingestion updates instead of duplicates.
            "id": f"{session_id}::{normalized_name}",
            "semantic_identifier": normalized_name,
            "sections": [{"text": text}],
            "source": "file",
            "metadata": {
                "session_id": session_id,
                "file_type": file_ext,
                "original_filename": filename,
            },
        },
        "cc_pair_id": ONYX_CC_PAIR_ID,
    }
    try:
        r = requests.post(
            f"{ONYX_BASE_URL}/onyx-api/ingestion",
            headers=ONYX_HEADERS,
            json=payload,
            timeout=30,
        )
        return r.status_code == 200
    except requests.RequestException:
        return False
