from pathlib import Path

from crewai import Agent, LLM
from config import MODEL

SKILLS_DIR = Path(__file__).parent.parent / "skills"


def make_report_writer() -> Agent:
    """Create the Report Writer agent."""
    llm = LLM(model=MODEL, temperature=0.3, top_p=0.9)
    return Agent(
        role="Professional Report Writer",
        goal=(
            "Convert the analytical report into a detailed, comprehensive, well-structured Markdown report. "
            "Follow the section order exactly. Include every source URL from the summary."
        ),
        backstory=(
            "You are a disciplined technical writer. Your rules: "
            "(1) Use ONLY information from the analytical report — add nothing new. "
            "(2) Follow the required section order: Title, Executive Summary, Key Themes, "
            "Evidence Quality, Identified Gaps, Conclusion. "
            "(3) Do NOT write a Sources section — it is appended automatically after your output. "
            "(4) Do not invent or guess URLs. Where you reference a source inline, "
            "use plain parenthetical citations matching the URLs in the summary. "
            "(5) If the analytical report contains a CONTRADICTION block, include it in the "
            "relevant theme section under a `#### Conflicting Evidence` heading. "
            "(6) Write in plain professional prose. Do not use bullet-only sections. "
            "Each section must have at least more than one full paragraph."
        ),
        llm=llm,
        verbose=True,
        skills=[str(SKILLS_DIR)],
    )