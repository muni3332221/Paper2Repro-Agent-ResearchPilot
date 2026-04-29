from pathlib import Path

from paper2repro.models import CodePlan, ExperimentResult, ReproPlan, SummaryResult, ValidationPlan
from paper2repro.reporter import write_report, write_starter_project


def sample_plan() -> ReproPlan:
    return ReproPlan(
        summary=SummaryResult(
            title="Demo Paper",
            problem="Problem",
            core_contribution="Contribution",
            method_overview="Method",
        ),
        experiment=ExperimentResult(datasets=["MNIST"], baselines=["CNN"], metrics=["accuracy"]),
        code_plan=CodePlan(framework="python", files={"README.md": "# Demo"}, commands=["python train.py"]),
        validation=ValidationPlan(checklist=["Check data"], expected_artifacts=["logs"], risk_items=["risk"]),
    )


def test_write_outputs(tmp_path: Path) -> None:
    plan = sample_plan()
    report = write_report(plan, tmp_path)
    project = write_starter_project(plan, tmp_path)
    assert report.exists()
    assert (tmp_path / "repro_plan.json").exists()
    assert (project / "README.md").exists()
