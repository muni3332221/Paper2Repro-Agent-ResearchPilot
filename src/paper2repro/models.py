from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class PaperSection(BaseModel):
    title: str
    content: str


class PaperDocument(BaseModel):
    source_path: str
    title: str = "Untitled Paper"
    abstract: str = ""
    sections: list[PaperSection] = Field(default_factory=list)
    raw_text: str = ""


class SummaryResult(BaseModel):
    title: str
    problem: str
    core_contribution: str
    method_overview: str
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ExperimentResult(BaseModel):
    task_type: str = "unknown"
    datasets: list[str] = Field(default_factory=list)
    baselines: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    hyperparameters: dict[str, str] = Field(default_factory=dict)
    compute_requirements: list[str] = Field(default_factory=list)
    implementation_notes: list[str] = Field(default_factory=list)


class CodePlan(BaseModel):
    framework: Literal["pytorch", "python", "jax", "tensorflow", "unknown"] = "python"
    files: dict[str, str] = Field(default_factory=dict)
    commands: list[str] = Field(default_factory=list)


class ValidationPlan(BaseModel):
    checklist: list[str] = Field(default_factory=list)
    expected_artifacts: list[str] = Field(default_factory=list)
    risk_items: list[str] = Field(default_factory=list)


class ReproPlan(BaseModel):
    summary: SummaryResult
    experiment: ExperimentResult
    code_plan: CodePlan
    validation: ValidationPlan
    token_estimate: str = "50k-200k tokens per paper, depending on paper length and code generation depth"


class RunConfig(BaseModel):
    pdf_path: Path
    output_dir: Path
    use_llm: bool = True
    model: str = "gpt-4o-mini"
    max_chars: int = 50000
