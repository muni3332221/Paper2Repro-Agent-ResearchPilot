from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Template

from .models import ReproPlan

REPORT_TEMPLATE = Template(
    """# Paper2Repro Report: {{ plan.summary.title }}

## 1. Problem
{{ plan.summary.problem }}

## 2. Core Contribution
{{ plan.summary.core_contribution }}

## 3. Method Overview
{{ plan.summary.method_overview }}

## 4. Experiment Extraction

### Task Type
{{ plan.experiment.task_type }}

### Datasets
{% for item in plan.experiment.datasets %}- {{ item }}
{% endfor %}
### Baselines
{% for item in plan.experiment.baselines %}- {{ item }}
{% endfor %}
### Metrics
{% for item in plan.experiment.metrics %}- {{ item }}
{% endfor %}
### Hyperparameters
{% if plan.experiment.hyperparameters %}{% for key, value in plan.experiment.hyperparameters.items() %}- {{ key }}: {{ value }}
{% endfor %}{% else %}- not specified
{% endif %}
### Compute Requirements
{% for item in plan.experiment.compute_requirements %}- {{ item }}
{% endfor %}

## 5. Reproduction Commands
{% for command in plan.code_plan.commands %}```bash
{{ command }}
```
{% endfor %}

## 6. Validation Checklist
{% for item in plan.validation.checklist %}- [ ] {{ item }}
{% endfor %}

## 7. Expected Artifacts
{% for item in plan.validation.expected_artifacts %}- {{ item }}
{% endfor %}

## 8. Risks
{% for item in plan.validation.risk_items %}- {{ item }}
{% endfor %}

## 9. Token Plan
{{ plan.token_estimate }}
"""
)


def write_report(plan: ReproPlan, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "repro_plan.md"
    report_path.write_text(REPORT_TEMPLATE.render(plan=plan), encoding="utf-8")
    (output_dir / "repro_plan.json").write_text(
        json.dumps(plan.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return report_path


def write_starter_project(plan: ReproPlan, output_dir: Path) -> Path:
    project_dir = output_dir / "starter_project"
    project_dir.mkdir(parents=True, exist_ok=True)
    for rel_path, content in plan.code_plan.files.items():
        target = project_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return project_dir
