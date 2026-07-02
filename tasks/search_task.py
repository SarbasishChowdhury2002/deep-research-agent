from crewai import Agent, Task


def make_search_task(researcher: Agent, query: str, session_id: str = "") -> Task:
    # pdf_text: str | None = None  # pdf-direct — on hold (Onyx ingestion used instead)
    session_fragment = f" session_id:{session_id}" if session_id else ""
    indexed_query = f"{query}{session_fragment}".strip()
    # Fallback step (kept for quick rollback, currently disabled):
    # doc_step = (
    #     f"STEP 3 — Uploaded document: The user has uploaded a document. "
    #     f"Read the content below and extract all relevant information for the query.\n\n"
    #     f"--- DOCUMENT START ---\n{pdf_text}\n--- DOCUMENT END ---\n\n"
    #     if pdf_text
    #     else "STEP 3 — No uploaded document for this session, skip this step.\n\n"
    # )
    doc_step = (
        "STEP 4 — Indexed documents: Call search_indexed_documents exactly using "
        f'query="{indexed_query}", limit=5.\n'
        "By default source_types filter — searches ALL connected sources configured "
        "in the knowledge base.\n"
        "For each returned chunk, note its source type if visible and label it "
        "[INTERNAL:<source_type>] (e.g. [INTERNAL:file], [INTERNAL:slack]). "
        "Use [INTERNAL] if the source type is not shown. "
        "Use any relevant chunks as evidence.\n\n"
    )
    return Task(
        description=(
            f"Your task: research this query and collect findings details and insights with source URLs.\n"
            f"QUERY: {query}\n\n"
            "Execute these steps IN ORDER. Do not skip any step.\n\n"
            "STEP 1 — Web search (exact): Call search_web with "
            f'query="{query}" and limit=5. Label these results [WEB-A].\n\n'
            "STEP 2 — Web search (expanded): Call search_web again with an expanded version "
            "of the query — add related terms, synonyms, or rephrase for broader/narrower coverage. "
            "Always pass limit=5. Label these results [WEB-B]. "
            "Deduplicate URLs across [WEB-A] and [WEB-B] before the next step.\n\n"
            "STEP 3 — Read top sources: From the combined deduplicated results, pick the 5 most "
            "relevant URLs. Call open_urls with those URLs to get their full content.\n\n"
            + doc_step
            + "STEP 5 — Compile findings: Write a structured list of findings as detailed and comprehensive possible.\n"
            "  - For each findings, write them word-by-word then immediately write its source URL in parentheses.\n"
            "  - Example: 'Hybrid search improves recall by 15%%...  (https://example.com/study)'\n"
            "  - Label web sources [WEB] and internal sources [INTERNAL].\n"
            "  - If two sources say different things about the same topic, write:\n"
            "    CONTRADICTION: Source A says [X] (url-A). Source B says [Y] (url-B).\n"
            "  - Do not add any information not found in the sources.\n\n"
            "STOP after completing Step 5. Do not write a report or summary."
        ),
        expected_output=(
            "A structured list of research findings report with raw details. Each finding must include:\n"
            "- The finding\n"
            "- Its source URL in parentheses, labelled [WEB] or [INTERNAL]\n"
            "- Any contradictions between sources clearly flagged as CONTRADICTION blocks.\n"
            "No narrative prose. No invented information. URLs must be real."
        ),
        agent=researcher,
    )
