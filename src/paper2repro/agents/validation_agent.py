from __future__ import annotations

from paper2repro.models import ExperimentResult, SummaryResult, ValidationPlan

from .base import AgentContext

SYSTEM = """You are Validation Agent. Build a reproducibility checklist.
Return strict JSON with keys: checklist, expected_artifacts, risk_items.
"""


class ValidationAgent:
    def __init__(self, context: AgentContext) -> None:
        self.context = context

    def run(self, summary: SummaryResult, experiment: ExperimentResult) -> ValidationPlan:
        if self.context.use_llm:
            prompt = f"Summary: {summary.model_dump_json()}\nExperiment: {experiment.model_dump_json()}"
            parsed = self.context.llm.complete_json(SYSTEM, prompt, ValidationPlan)
            if parsed:
                return parsed

        return ValidationPlan(
            checklist=[
                "Confirm dataset source, version, license, and preprocessing steps.",
                "Reproduce at least one main table or figure before extending the experiment.",
                "Match random seeds, batch size, learning rate, optimizer, and number of epochs.",
                "Run baseline models under the same data split and metric implementation.",
                "Log environment details: Python version, dependency versions, GPU/CPU, and OS.",
            ],
            expected_artifacts=[
                "configs/experiment.yaml",
                "training logs",
                "evaluation metrics table",
                "reproduction notes with deviations from the paper",
            ],
            risk_items=[
                "Important details may be hidden in appendix, figures, tables, or released code.",
                "Dataset preprocessing differences can dominate final scores.",
                "Compute budget may not match the paper's original setup.",
            ],
        )
