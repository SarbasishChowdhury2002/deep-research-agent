"""Deep Research Flow — three-stage CrewAI Flow (search → analyse → report).

Each stage runs as its own single-agent Crew so agents stay focused.
The MCPServerAdapter is held open for the full flow duration.
"""

import queue
import re
import threading
from typing import Callable, Generator

from crewai import Crew, Process
from crewai.flow.flow import Flow, listen, start
from crewai_tools import MCPServerAdapter

from agents.analyst import make_analyst
from agents.report_writer import make_report_writer
from agents.researcher import make_researcher
from config import ONYX_TOKEN, ONYX_MCP_URL
from tasks.analysis_task import make_analysis_task
from tasks.report_task import make_report_task
from tasks.search_task import make_search_task
from utils.url_utils import extract_urls


class ResearchFlow(Flow):
    """Search → Analyse → Report, each stage its own mini-crew."""

    def __init__(
        self,
        query: str,
        mcp_tools: list,
        session_id: str = "",
        status_callback: Callable[[str], None] | None = None,
        # pdf_text: str | None = None,  # pdf-direct — on hold (Onyx ingestion used instead)
    ):
        super().__init__()
        self.query = query
        self.mcp_tools = mcp_tools
        self.session_id = session_id
        self.status_callback = status_callback
        # self.pdf_text = pdf_text
        self._collected_urls: list[str] = []

    # ── Stage 1: Search ───────────────────────────────────────────────────────
    @start()
    def search(self) -> str:
        if self.status_callback:
            self.status_callback("researcher")

        for tool in self.mcp_tools:
            original_run = tool._run
            url_store = self._collected_urls

            def _make_capturing_run(orig, store):
                def _run(**kwargs):
                    result = orig(**kwargs)
                    for url in extract_urls(str(result)):
                        if url not in store:
                            store.append(url)
                    return result
                return _run

            tool._run = _make_capturing_run(original_run, url_store)

        researcher = make_researcher(self.mcp_tools)
        task = make_search_task(researcher, self.query, self.session_id)
        # pdf_text=self.pdf_text — on hold
        crew = Crew(agents=[researcher], tasks=[task], process=Process.sequential, verbose=True)
        result = crew.kickoff(inputs={"query": self.query, "session_id": self.session_id})
        return result.raw if hasattr(result, "raw") else str(result)

    # ── Stage 2: Analyse ──────────────────────────────────────────────────────
    @listen(search)
    def analyse(self, search_results: str) -> str:
        if self.status_callback:
            self.status_callback("analyst")
        analyst = make_analyst()
        task = make_analysis_task(analyst)
        crew = Crew(agents=[analyst], tasks=[task], process=Process.sequential, verbose=True)
        result = crew.kickoff(inputs={"research_findings": search_results})
        return result.raw if hasattr(result, "raw") else str(result)

    # ── Stage 3: Write report ─────────────────────────────────────────────────
    @listen(analyse)
    def write_report(self, analysis_results: str) -> str:
        if self.status_callback:
            self.status_callback("writer")
        report_writer = make_report_writer()
        task = make_report_task(report_writer)
        crew = Crew(agents=[report_writer], tasks=[task], process=Process.sequential, verbose=True)
        result = crew.kickoff(inputs={"analytical_summary": analysis_results})
        report = result.raw if hasattr(result, "raw") else str(result)

        if self._collected_urls:
            report = re.sub(r"\n##+ Sources.*", "", report, flags=re.DOTALL).rstrip()
            sources_lines = "\n".join(f"- <{u}>" for u in self._collected_urls)
            report = f"{report}\n\n## Sources\n{sources_lines}\n"

        return report


def run_research_sync(
    query: str,
    session_id: str = "",
    status_callback: Callable[[str], None] | None = None,
    # pdf_text: str | None = None,  # pdf-direct — on hold
) -> str:
    """
    Run the ResearchFlow and return the final report string directly.
    """
    mcp_params = {
        "url": ONYX_MCP_URL,
        "headers": {"Authorization": f"Bearer {ONYX_TOKEN}"},
        "transport": "streamable-http",
    }
    with MCPServerAdapter(mcp_params) as mcp:
        flow = ResearchFlow(
            query=query,
            mcp_tools=list(mcp),
            session_id=session_id,
            status_callback=status_callback,
            # pdf_text=pdf_text,  # on hold
        )
        final = flow.kickoff()
        return final if isinstance(final, str) else str(final)


_STATUS_PREFIX = "\x00STATUS\x00"


def run_research(
    query: str,
    session_id: str = "",
    status_callback: Callable[[str], None] | None = None,
    # pdf_text: str | None = None,  # pdf-direct — on hold
) -> Generator[str, None, str]:
    """
    Run the ResearchFlow and yield word tokens for streaming.

    Yield string tokens as each stage completes.
    The full report string is returned as StopIteration.value when the generator is exhausted.
    """
    mcp_params = {
        "url": ONYX_MCP_URL,
        "headers": {"Authorization": f"Bearer {ONYX_TOKEN}"},
        "transport": "streamable-http",
    }

    with MCPServerAdapter(mcp_params) as mcp:
        token_queue: queue.Queue = queue.Queue()
        full_text_holder = [""]

        def _run_flow():
            # Wrap the callback so status updates travel through the queue and
            # are dispatched from the generator thread (which holds Streamlit's
            # ScriptRunContext). Calling st.* directly from crewai's internal
            # ThreadPoolExecutor threads (used by @listen) raises a context error.
            def _queue_status(stage: str):
                token_queue.put(_STATUS_PREFIX + stage)

            try:
                flow = ResearchFlow(
                    query=query,
                    mcp_tools=list(mcp),
                    session_id=session_id,
                    status_callback=_queue_status,
                    # pdf_text=pdf_text,  # on hold
                )
                final = flow.kickoff()
                output = final if isinstance(final, str) else str(final)
                for word in output.split(" "):
                    token_queue.put(word + " ")
                full_text_holder[0] = output
                token_queue.put(_STATUS_PREFIX + "done")
            except Exception as exc:
                token_queue.put(f"\n\n**Error:** {exc}")
            finally:
                token_queue.put(None)  # sentinel

        thread = threading.Thread(target=_run_flow, daemon=True)
        thread.start()

        while True:
            token = token_queue.get()
            if token is None:
                break
            if isinstance(token, str) and token.startswith(_STATUS_PREFIX):
                stage = token[len(_STATUS_PREFIX):]
                if status_callback:
                    status_callback(stage)
            else:
                yield token

        thread.join(timeout=5)

    return full_text_holder[0]
