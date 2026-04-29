from __future__ import annotations

from paper2repro.heuristics import find_hyperparameters, find_keywords, sentences
from paper2repro.models import ExperimentResult, PaperDocument

from .base import AgentContext

SYSTEM = """You are Experiment Agent. Extract reproducibility information from a paper.
Return strict JSON with keys: task_type, datasets, baselines, metrics, hyperparameters,
compute_requirements, implementation_notes. Do not invent facts.
"""


class ExperimentAgent:
    def __init__(self, context: AgentContext) -> None:
        self.context = context

    def run(self, paper: PaperDocument) -> ExperimentResult:
        if self.context.use_llm:
            prompt = f"Title: {paper.title}\nPaper text:\n{paper.raw_text[:22000]}"
            parsed = self.context.llm.complete_json(SYSTEM, prompt, ExperimentResult)
            if parsed:
                return parsed

        text = paper.raw_text
        notes = sentences(text, 5)
        return ExperimentResult(
            task_type="machine-learning or computational experiment; verify manually",
            datasets=find_keywords(text, "datasets") or ["not specified"],
            baselines=find_keywords(text, "baselines") or ["not specified"],
            metrics=find_keywords(text, "metrics") or ["not specified"],
            hyperparameters=find_hyperparameters(text),
            compute_requirements=["not specified; estimate from model size and dataset scale"],
            implementation_notes=notes or ["Review method and experiment sections manually."],
        )
