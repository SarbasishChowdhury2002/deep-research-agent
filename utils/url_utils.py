"""Utility for extracting URLs from raw LLM / tool output text."""

import re

# Matches http/https URLs, stops at whitespace or common trailing punctuation
_URL_RE = re.compile(r'https?://[^\s\)\]\>"\']+')


def extract_urls(text: str) -> list[str]:
    """Return a deduplicated, ordered list of URLs found in *text*."""
    found = _URL_RE.findall(text)
    # Strip trailing punctuation that regex may have captured
    cleaned = [u.rstrip(".,;:") for u in found]
    # Deduplicate while preserving order
    seen: set[str] = set()
    result: list[str] = []
    for u in cleaned:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result
