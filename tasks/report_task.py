from crewai import Task
from crewai import Agent


def make_report_task(report_writer: Agent) -> Task:
    return Task(
        description=(
            "Your task: write a professional Markdown research report from the analytical report below.\n\n"
            "ANALYTICAL REPORT DETAILS:\n{analytical_summary}\n\n"
            "Write the report using EXACTLY this section order — do not skip or reorder:\n\n"
            "1. `# [Title]` — one concise sentence naming the research topic\n"
            "2. `## Executive Summary` — 3-5 sentences: research question, key findings, headline conclusion\n"
            "3. `## Key Themes and Insights` — one `### [Theme Name]` subsection per theme from the report. "
            "Each subsection needs at least two prose paragraphs.\n"
            "   - If a theme contains a CONTRADICTION block, add a `#### Conflicting Evidence` "
            "subsection that states both claims and their sources.\n"
            "4. `## Evidence Quality Assessment` — prose on source credibility per theme. "
            "Note the [WEB] vs [INTERNAL] split and the primary/secondary breakdown from the report.\n"
            "5. `## Identified Gaps` — bullet list of what the research could not answer, "
            "including any gaps in internal knowledge base coverage.\n"
            "6. `## Conclusion` — synthesise takeaways; introduce NO new information.\n\n"
            "RULES:\n"
            "- Use ONLY information from the analytical report. Add nothing new.\n"
            "- Write in plain professional prose. Each section must have at least more than one full paragraph.\n"
            "- Do not produce a bullet-only report.\n"
            "- Do NOT write a `## Sources` section — it will be appended automatically after your output.\n"
            "- Do not end your output with any sources list, URL list, or reference section of any kind."
        ),
        expected_output=(
            "A complete Markdown research report with exactly these sections in order: "
            "Title, Executive Summary, Key Themes and Insights (with theme subsections), "
            "Evidence Quality Assessment, Identified Gaps, and Conclusion. "
            "No Sources section and no URL list at the end — that is appended separately by the system."
        ),
        agent=report_writer,
    )
