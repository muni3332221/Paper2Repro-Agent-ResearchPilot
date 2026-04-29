from __future__ import annotations

from paper2repro.heuristics import likely_framework
from paper2repro.models import CodePlan, ExperimentResult, SummaryResult

from .base import AgentContext

SYSTEM = """You are Code Agent. Design a minimal reproducible project skeleton.
Return strict JSON with keys: framework, files, commands. files maps relative paths to file contents.
Keep generated code compact, runnable, and honest about TODOs.
"""


def default_files(summary: SummaryResult, exp: ExperimentResult) -> dict[str, str]:
    bullet_datasets = "\n".join(f"- {d}" for d in exp.datasets)
    bullet_baselines = "\n".join(f"- {b}" for b in exp.baselines)
    bullet_metrics = "\n".join(f"- {m}" for m in exp.metrics)
    return {
        "requirements.txt": "numpy\npandas\nscikit-learn\ntorch\ntqdm\n",
        "src/config.py": """from dataclasses import dataclass\n\n\n@dataclass\nclass ExperimentConfig:\n    dataset_name: str = \"TODO\"\n    seed: int = 42\n    batch_size: int = 32\n    learning_rate: float = 1e-3\n    epochs: int = 10\n""",
        "src/data.py": """from __future__ import annotations\n\n\ndef load_dataset(name: str):\n    \"\"\"Load or download the dataset described in the paper.\n\n    Replace this placeholder with the official dataset loader.\n    \"\"\"\n    raise NotImplementedError(f\"Dataset loader not implemented: {name}\")\n""",
        "src/model.py": """from __future__ import annotations\n\nimport torch\nfrom torch import nn\n\n\nclass ReproModel(nn.Module):\n    \"\"\"Placeholder model. Replace with the architecture from the paper.\"\"\"\n\n    def __init__(self, input_dim: int = 128, hidden_dim: int = 256, output_dim: int = 10):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Linear(input_dim, hidden_dim),\n            nn.ReLU(),\n            nn.Linear(hidden_dim, output_dim),\n        )\n\n    def forward(self, x):\n        return self.net(x)\n""",
        "src/train.py": """from __future__ import annotations\n\nfrom config import ExperimentConfig\n\n\ndef main() -> None:\n    cfg = ExperimentConfig()\n    print(\"Training placeholder. Fill in data/model/loss according to the paper.\")\n    print(cfg)\n\n\nif __name__ == \"__main__\":\n    main()\n""",
        "src/evaluate.py": """from __future__ import annotations\n\n\ndef main() -> None:\n    print(\"Evaluation placeholder. Implement metrics reported by the paper.\")\n\n\nif __name__ == \"__main__\":\n    main()\n""",
        "README.md": f"""# Reproduction Starter: {summary.title}\n\n## Goal\n{summary.core_contribution}\n\n## Datasets to verify\n{bullet_datasets}\n\n## Baselines to compare\n{bullet_baselines}\n\n## Metrics\n{bullet_metrics}\n\n## Quick start\n\n```bash\npython -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\npython src/train.py\npython src/evaluate.py\n```\n\n## Important TODOs\n- Replace placeholder model with the architecture described in the paper.\n- Implement official dataset preprocessing.\n- Match hyperparameters and random seeds from the experiment section.\n- Add scripts for each reported table or figure.\n""",
    }


class CodeAgent:
    def __init__(self, context: AgentContext) -> None:
        self.context = context

    def run(self, summary: SummaryResult, experiment: ExperimentResult, paper_text: str) -> CodePlan:
        if self.context.use_llm:
            prompt = (
                f"Summary: {summary.model_dump_json()}\n"
                f"Experiment: {experiment.model_dump_json()}\n"
                f"Paper excerpt: {paper_text[:12000]}"
            )
            parsed = self.context.llm.complete_json(SYSTEM, prompt, CodePlan)
            if parsed:
                return parsed

        framework = likely_framework(paper_text)
        return CodePlan(
            framework=framework if framework in {"pytorch", "python", "jax", "tensorflow"} else "python",
            files=default_files(summary, experiment),
            commands=[
                "python -m venv .venv",
                "source .venv/bin/activate",
                "pip install -r requirements.txt",
                "python src/train.py",
                "python src/evaluate.py",
            ],
        )
