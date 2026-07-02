"""CLI entry point for the Deep Research Agent (no UI).

Usage:
    python main.py "your research query here"
    python main.py  # will prompt for input
    Example: python main.py "Write a deep research report on how we should design our RAG retrieval layer for production. Use our internal proposed methods/discussions in Slack, our private benchmark/experiment results in Notion, and the technical theory PDF as sources alongside web research."
"""

import sys
import os

# Ensure project root is on the path so relative imports work.
sys.path.insert(0, os.path.dirname(__file__))

from crew.research_crew import run_research_sync


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your research query: ").strip()

    if not query:
        print("No query provided. Exiting.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Research query: {query}")
    print(f"{'='*60}\n")

    def on_status(stage: str):
        print(f"\n[STATUS] {stage}\n", flush=True)

    full_report = run_research_sync(query, status_callback=on_status)
    print(full_report)

    print(f"\n\n{'='*60}")
    print("Research complete.")
    print(f"{'='*60}\n")

    # Optionally save to file
    output_file = "report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_report)
    print(f"Report saved to {output_file}")


if __name__ == "__main__":
    main()
