"""Deep Research Agent — Streamlit entry point."""

import base64
import uuid

import streamlit as st
from streamlit_mic_recorder import mic_recorder

st.set_page_config(
    page_title="Agentic Deep Researcher",
    page_icon="🔬",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    .stApp { background-color: #0d0f14; }

    header[data-testid="stHeader"] {
        background-color: #0d0f14 !important;
        border-bottom: 1px solid #1c1f2b;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebarContent"] { background-color: #13151c; }

    pre, code {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        max-width: 100% !important;
    }
    div[data-testid="stCodeBlock"] {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }

    section.main > div { padding-bottom: 80px !important; }

    .pdf-preview iframe {
        height: 300px !important;
        width: 100% !important;
        border-radius: 8px;
        border: none;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "audio_bytes" not in st.session_state:
    st.session_state["audio_bytes"] = None
if "is_researching" not in st.session_state:
    st.session_state["is_researching"] = False
if "uploaded_pdf" not in st.session_state:
    st.session_state["uploaded_pdf"] = None
if "voice_draft" not in st.session_state:
    st.session_state["voice_draft"] = ""
if "pending_prompt" not in st.session_state:
    st.session_state["pending_prompt"] = None


def reset_chat():
    st.session_state["messages"] = []
    st.session_state["audio_bytes"] = None
    st.session_state["is_researching"] = False
    st.session_state["voice_draft"] = ""
    st.session_state["uploaded_pdf"] = None
    st.session_state["pending_prompt"] = None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Documents")

    with st.container(border=True, width="content"):
        uploaded = st.file_uploader(
            "Drag and drop your file here",
            type=["pdf"],
            label_visibility="visible",
        )

    if uploaded:
        if (
            st.session_state["uploaded_pdf"] is None
            or st.session_state["uploaded_pdf"]["name"] != uploaded.name
        ):
            pdf_data = uploaded.read()
            with st.spinner("Indexing document…"):
                from utils.file_utils import extract_text
                from services.onyx_service import ingest_document

                text = extract_text(pdf_data, uploaded.name)
                ok = ingest_document(
                    uploaded.name, text, st.session_state["session_id"]
                )

            st.session_state["uploaded_pdf"] = {
                "name": uploaded.name,
                "status": "ready" if ok else "error",
                "data": pdf_data,
                "text": text,
            }

    if st.session_state["uploaded_pdf"]:
        doc = st.session_state["uploaded_pdf"]
        icon = "✓" if doc["status"] == "ready" else "✗"
        st.success(f"{icon} {doc['name']}")
        b64 = base64.b64encode(doc["data"]).decode("utf-8")
        st.markdown(
            f"<div class='pdf-preview'>"
            f"<iframe src='data:application/pdf;base64,{b64}'></iframe>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Voice recorder ────────────────────────────────────────────────────────
    st.divider()
    st.header("🎙 Voice Input")

    audio = mic_recorder(
        start_prompt="🔴 Record your question",
        stop_prompt="⏹ Stop",
        use_container_width=True,
        just_once=True,
        key="mic",
    )

    if audio:
        with st.spinner("Transcribing…"):
            from services.stt_service import transcribe

            text = transcribe(audio["bytes"])
        if text:
            st.session_state["voice_draft"] = text
            st.rerun()
        else:
            st.warning("⚠️ Could not understand audio. Please try again.")

    if st.session_state["voice_draft"]:
        st.caption("Transcribed — edit below before sending:")
        edited = st.text_area(
            label="voice_edit",
            value=st.session_state["voice_draft"],
            height=100,
            label_visibility="collapsed",
        )
        col_send, col_discard = st.columns(2)
        with col_send:
            if st.button("↑ Send", use_container_width=True, type="primary"):
                st.session_state["pending_prompt"] = edited
                st.session_state["voice_draft"] = ""
                st.rerun()
        with col_discard:
            if st.button("✕ Discard", use_container_width=True):
                st.session_state["voice_draft"] = ""
                st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_clear = st.columns([10, 1], gap="small", vertical_alignment="center")
with col_title:
    st.header("🔬 Agentic Deep Researcher")
    powered_by_html = """
    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
        <span style='font-size: 20px; color: #666;'>Powered by</span>
        <img src="https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg" width="80"> 
        <span style='font-size: 20px; color: #666;'>and</span>
        <img src="https://mintcdn.com/danswer/1bxGRwgOacJPGlC5/assets/logo/onyx_logo_inverted.svg?fit=max&auto=format&n=1bxGRwgOacJPGlC5&q=85&s=9cddb5f01462839d08ffc43a57a40f11" width="90">
        <span style='font-size: 20px; color: #666;'>and</span>
        <img src="https://cdn-avatars.huggingface.co/v1/production/uploads/634c17653d11eaedd88b314d/9OgyfKstSZtbmsmuG8MbU.png" width="35">
    </div>
    """
    st.markdown(powered_by_html, unsafe_allow_html=True)
with col_clear:
    st.button("Clear ↺", on_click=reset_chat)

# ── Chat history ──────────────────────────────────────────────────────────────
for i, message in enumerate(st.session_state["messages"]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and i == len(st.session_state["messages"]) - 1
        ):
            st.write("")
            play_col, _ = st.columns([2, 8])
            with play_col:
                if st.button("▶ Play Report", key=f"tts_{i}", use_container_width=True):
                    from services.tts_service import synthesise_report

                    with st.spinner("Generating audio…"):
                        audio_out = synthesise_report(message["content"])
                    st.session_state["audio_bytes"] = audio_out

            if st.session_state["audio_bytes"]:
                st.audio(st.session_state["audio_bytes"], format="audio/mp3")

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input(
    "Ask anything to research…",
    disabled=st.session_state["is_researching"],
)

# ── Resolve prompt ────────────────────────────────────────────────────────────
prompt = None
if user_input and user_input.strip():
    prompt = user_input.strip()
elif st.session_state["pending_prompt"]:
    prompt = st.session_state["pending_prompt"]
    st.session_state["pending_prompt"] = None

# ── Research pipeline ─────────────────────────────────────────────────────────
if prompt:
    st.session_state["audio_bytes"] = None
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_text = st.empty()
        status_text.info("⚙️ **Researcher Agent** — gathering information…")

        from crew.research_crew import run_research

        def on_stage(stage: str):
            if stage == "analyst":
                status_text.info("⚙️ **Analyst Agent** — synthesising findings…")
            elif stage == "writer":
                status_text.info("⚙️ **Report Writer** — composing report…")
            elif stage == "done":
                status_text.success("✅ Research complete.")

        st.session_state["is_researching"] = True
        # Fallback (direct PDF text pass-through) kept intact but disabled for now.
        # pdf_text = (
        #     st.session_state["uploaded_pdf"].get("text")
        #     if st.session_state["uploaded_pdf"]
        #     else None
        # )
        token_gen = run_research(
            prompt,
            session_id=st.session_state["session_id"],
            status_callback=on_stage,
            # pdf_text=pdf_text,
        )
        full_text = st.write_stream(token_gen)
        st.session_state["is_researching"] = False

    st.session_state["messages"].append({"role": "assistant", "content": full_text})
    st.rerun()
