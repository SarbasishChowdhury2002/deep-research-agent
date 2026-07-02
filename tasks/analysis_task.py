from crewai import Task
from crewai import Agent


def make_analysis_task(analyst: Agent) -> Task:
    return Task(
        description=(
            "Your task: analyse and synthesise the research findings below into a structured analytical report.\n\n"
            "RESEARCH FINDINGS:\n{research_findings}\n\n"
            "Execute these steps IN ORDER:\n\n"
            "STEP 1 — Deduplicate: If the same details appears from multiple sources, "
            "merge them into one point and list all source URLs together.\n\n"
            "STEP 2 — Flag contradictions: If sources disagree on a finding, write a block:\n"
            "  CONTRADICTION: [topic]\n"
            "  - Claim A: [what source A says] (source-A-url)\n"
            "  - Claim B: [what source B says] (source-B-url)\n\n"
            "STEP 3 — Group into themes: Organise all findings into 3-5 named themes. "
            "Each theme gets a heading. Under each theme, list every insights with their URLs.\n\n"
            "STEP 4 — Assess evidence quality per theme:\n"
            "  - Distinguish [WEB] sources from [INTERNAL] sources.\n"
            "  - Classify each source as primary (original studies, official documentation, "
            "internal records, raw data) or secondary (blogs, summaries, aggregators).\n"
            "  - Give the theme an overall evidence rating: strong (mostly primary, consistent), "
            "mixed (combination of primary/secondary, or minor inconsistencies), "
            "or weak (secondary only, thin coverage, or major gaps).\n"
            "  - If [INTERNAL] sources are present, note them explicitly — they represent "
            "organisation-specific knowledge and should be weighted accordingly.\n\n"
            "STEP 5 — List gaps: State what the research could NOT answer or did not cover. "
            "Include both gaps in web coverage and gaps in internal knowledge base coverage.\n\n"
            "STEP 6 — Preserve all URLs: Copy every source URL from the research findings "
            "into your report. Do not drop, modify, or invent any URL.\n\n"
            "Do not add information not present in the research findings."
        ),
        expected_output=(
            "A structured comprehensive analytical report containing:\n"
            "- 3-5 named theme sections, each with every insights/findings and source URLs\n"
            "- Any CONTRADICTION blocks for conflicting sources\n"
            "- An evidence quality note per theme (strong / mixed / weak, "
            "with [WEB] vs [INTERNAL] breakdown)\n"
            "- A Gaps section listing unanswered questions\n"
            "- All source URLs preserved verbatim from the research findings"
        ),
        agent=analyst,
    )
