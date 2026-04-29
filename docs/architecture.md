# Architecture

Paper2Repro Agent uses a simple multi-agent pipeline. Each stage has one responsibility and passes structured data to the next stage.

```text
PDF file
  ↓
PDF Parser
  ↓
PaperDocument
  ↓
Summary Agent ─────┐
  ↓                │
Experiment Agent ──┤
  ↓                │
Code Agent ────────┤
  ↓                │
Validation Agent ──┘
  ↓
Reporter
  ↓
repro_plan.md + repro_plan.json + starter_project/
```

## Components

### PDF Parser

Extracts text from PDF files with `pypdf`, infers a title, and splits the paper into approximate sections.

### Summary Agent

Extracts the problem, core contribution, method overview, assumptions, and limitations. In LLM mode, it requests strict JSON. In offline mode, it uses sentence-level heuristics.

### Experiment Agent

Extracts reproducibility details such as datasets, baselines, metrics, hyperparameters, compute requirements, and implementation notes.

### Code Agent

Generates a starter project. The generated files are intentionally conservative: they provide a scaffold rather than pretending to exactly reproduce the paper without human verification.

### Validation Agent

Creates a checklist, expected artifacts, and risk items so the user can verify whether the reproduction is faithful.

### Reporter

Writes the final Markdown report, JSON plan, and starter project files.

## Design principle

The project prioritizes verifiable planning over overconfident code generation. The system should make reproduction easier, but the user should still verify every important detail against the original paper and any official code or dataset documentation.
