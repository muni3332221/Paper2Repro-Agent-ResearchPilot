from __future__ import annotations

from paper2repro.heuristics import sentences
from paper2repro.models import PaperDocument, SummaryResult

from .base import AgentContext

SYSTEM = """You are Summary Agent. Extract a concise research-paper summary.
Return strict JSON with keys: title, problem, core_contribution, method_overview, assumptions, limitations.
Do not invent facts. Use 'not specified' when missing.
"""


class SummaryAgent:
    def __init__(self, context: AgentContext) -> None:
        self.context = context

    def run(self, paper: PaperDocument) -> SummaryResult:
        if self.context.use_llm:
            prompt = f"Title: {paper.title}\nAbstract: {paper.abstract}\nText:\n{paper.raw_text[:18000]}"
            parsed = self.context.llm.complete_json(SYSTEM, prompt, SummaryResult)
            if parsed:
                return parsed

        sample = sentences(paper.abstract or paper.raw_text, 6)
        return SummaryResult(
            title=paper.title,
            problem=sample[0] if sample else "The paper's problem statement was not clearly extracted.",
            core_contribution=sample[1] if len(sample) > 1 else "Core contribution requires manual verification.",
            method_overview=" ".join(sample[2:4]) if len(sample) > 3 else "Method overview requires manual verification.",
            assumptions=["Verify assumptions against the original PDF before running experiments."],
            limitations=["Heuristic mode may miss details hidden in figures, tables, or equations."],
        )
