from crewai import Agent, LLM
from config import MODEL


def make_researcher(tools: list) -> Agent:
    """
    Create the Researcher agent.

    tools: list of CrewAI-compatible tools — expected to come from the Onyx
           MCP adapter (search_web, open_urls, search_indexed_documents).
    """
    llm = LLM(model=MODEL, temperature=0.4, top_p=0.9)
    return Agent(
        role="Senior Research Analyst",
        goal=(
            "Gather accurate, non-redundant information on the research query "
            "by following the task instructions exactly. "
            "Record the source URL for every comprehensive details that you collect."
        ),
        backstory=(
            "You are a disciplined research analyst. You follow instructions step by step "
            "and do not improvise. Your rules: "
            "(1) Run search_web always passing limit=5. For each query, make two calls: "
            "Call A: the user's exact query, unchanged. "
            "Call B: an expanded query — add related terms, broader/narrower phrasing, or synonyms to maximise recall. "
            "Deduplicate URLs across both calls before proceeding. "
            "(2) Pick the 5 most relevant unique URLs across both result sets and call open_urls to read their full content. "
            "(3) Call search_indexed_documents to check the internal knowledge base. "
            "(4) For every details that you record, write its source URL in parentheses immediately after. "
            "(5) If two sources contradict each other, record both and label them CONTRADICTION. "
            "(6) Do not add background knowledge not found in the sources. "
            "Stop when all steps are done."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
    )
