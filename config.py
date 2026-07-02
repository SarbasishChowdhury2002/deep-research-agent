import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MODEL = "ollama/gemma4:26b"

ONYX_BASE_URL = "https://cloud.onyx.app/api"
ONYX_MCP_URL = "https://cloud.onyx.app/mcp"
ONYX_TOKEN = os.getenv("ONYX_TOKEN", "")
ONYX_API_KEY = os.getenv("ONYX_API_KEY", "")
ONYX_CC_PAIR_ID = 36        # Change it to your Connector ID https://docs.onyx.app/developers/guides/index_files_ingestion_api

ONYX_HEADERS = {
    "Authorization": f"Bearer {ONYX_API_KEY}",
    "Content-Type": "application/json",
}

VOXTRAL_VOICE = "gb_jane_neutral"
