---
name: deep-research-report
description: >
  Guidelines for writing high-quality, publication-ready deep research reports.
  Covers structure, tone, evidence standards, and formatting rules so the agent
  consistently produces clear, credible, and well-organised Markdown reports.
metadata:
  author: deep-research-agent
  version: "1.1"
---

# Deep Research Report Writing Guidelines

## Report Structure

Always follow this section order exactly. Never skip or reorder sections.

1. **Title** — `# Title` — one concise sentence naming the research topic.
2. **Executive Summary** — `## Executive Summary` — 3–5 sentences covering the research
   question, key findings, and headline conclusion. No new claims beyond what the body contains.
3. **Key Themes and Insights** — `## Key Themes and Insights` — contains one `### [Theme Name]`
   subsection per major theme. This is the most detailed section. Each theme subsection must
   contain at least two prose paragraphs with distinct supporting points. If a theme has
   conflicting evidence, add a `#### Conflicting Evidence` subsection within that theme.
4. **Evidence Quality Assessment** — `## Evidence Quality Assessment` — prose evaluation of
   source credibility per theme. Note the split between `[WEB]` and `[INTERNAL]` sources,
   and distinguish primary sources (studies, official docs, internal records) from secondary
   sources (blogs, summaries). Rate each theme: **strong**, **mixed**, or **weak**.
5. **Identified Gaps** — `## Identified Gaps` — bullet list of what the research could not
   answer, including gaps in both web coverage and internal knowledge base coverage.
6. **Conclusion** — `## Conclusion` — synthesised takeaway only. Introduce no new information.
7. **Sources** — `## Sources` — this section is appended automatically by the system after
   your output. **Do not write it yourself.** Do not end your report with any URL list,
   reference section, or sources block of any kind.

## Heading Hierarchy

```
# Report Title
## Executive Summary
## Key Themes and Insights
### Theme One Name
#### Conflicting Evidence   (only if contradictions exist in this theme)
### Theme Two Name
## Evidence Quality Assessment
## Identified Gaps
## Conclusion
```

Never use `##` for individual themes — they are always `###` inside `## Key Themes and Insights`.

## Writing Style

- Use **plain, professional English**. Avoid jargon unless the audience requires it; define terms on first use.
- Write in the **third person**. Do not use "I", "we", or "our team".
- Keep sentences concise (≤ 25 words where possible). Break long chains of clauses into
  separate sentences or paragraphs.
- **Active voice** is preferred: "The study found X" not "X was found by the study".
- Avoid filler openers: "It is worth noting that…", "Interestingly…", "In conclusion…"
  at the start of paragraphs.

## Headings and Formatting

- Top-level title: `#`
- Major sections: `##`
- Theme subsections: `###`
- Conflicting evidence blocks: `####`
- Use **bold** for key terms on first mention only, not for decoration.
- Use bullet lists for 3+ parallel items; use prose for fewer.
- Use numbered lists only for ranked items or sequential steps.
- Do not use tables unless comparing ≥ 3 items across ≥ 2 dimensions.
- No horizontal rules (`---`) inside the report body.

## Evidence and Citations

- Every factual claim must be followed by an inline parenthetical citation: `(url)`
- If multiple sources support the same claim, list all URLs in the same parenthetical:
  `(url-1, url-2)`.
- Do not fabricate URLs. If a source URL is unknown, write `(source name — URL unavailable)`.
- Flag secondary sources (blogs, summaries, aggregators) explicitly with the label
  `[secondary source]` after the citation.
- Use hedging language when evidence is weak or conflicting: "suggests", "indicates",
  "according to [source]".

## Depth and Completeness

- Each `### Theme` section must contain at least two distinct supporting points, each
  with its own evidence.
- Do not pad sections with background knowledge the reader already has. Get to the insight quickly.
- The Executive Summary must not introduce claims absent from the body.
- The Conclusion must not introduce new evidence; it synthesises only what appears above.

## What to Avoid

- Do not produce bullet-only reports. Prose paragraphs must anchor every section.
- Do not repeat the same finding across multiple sections.
- Do not use vague superlatives — "best", "most powerful", "revolutionary" — unless
  directly quoting a source.
- Do not include code blocks unless the topic is explicitly technical.
- Do not invent statistics. If a number is unavailable, say so explicitly.
- Do not write a Sources section. It is added by the system automatically.
