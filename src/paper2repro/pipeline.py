from __future__ import annotations

from .agents.base import AgentContext
from .agents.code_agent import CodeAgent
from .agents.experiment_agent import ExperimentAgent
from .agents.summary_agent import SummaryAgent
from .agents.validation_agent import ValidationAgent
from .llm import LLMClient
from .models import ReproPlan, RunConfig
from .pdf_parser import parse_pdf
from .reporter import write_report, write_starter_project


def run_pipeline(config: RunConfig) -> ReproPlan:
    paper = parse_pdf(config.pdf_path, config.max_chars)
    context = AgentContext(llm=LLMClient(config.model), use_llm=config.use_llm)

    summary = SummaryAgent(context).run(paper)
    experiment = ExperimentAgent(context).run(paper)
    code_plan = CodeAgent(context).run(summary, experiment, paper.raw_text)
    validation = ValidationAgent(context).run(summary, experiment)

    plan = ReproPlan(
        summary=summary,
        experiment=experiment,
        code_plan=code_plan,
        validation=validation,
    )
    write_report(plan, config.output_dir)
    write_starter_project(plan, config.output_dir)
    return plan
