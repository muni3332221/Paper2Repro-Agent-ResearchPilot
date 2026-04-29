# Token Plan

Paper2Repro Agent can run in two modes.

## Offline mode

Offline mode uses local PDF parsing and heuristic extraction.

```bash
paper2repro run path/to/paper.pdf --no-llm -o outputs/demo
```

Estimated LLM token cost: **0 tokens**.

## LLM mode

LLM mode uses structured extraction for higher-quality results.

```bash
paper2repro run path/to/paper.pdf -o outputs/demo
```

Estimated token budget per paper:

| Stage | Estimated tokens |
|---|---:|
| Summary Agent | 10k–40k |
| Experiment Agent | 20k–80k |
| Code Agent | 10k–60k |
| Validation Agent | 5k–20k |
| Total | 50k–200k |

The exact number depends on PDF length, selected model, context-window size, and how much starter code is generated.

## Cost-control ideas

- Use `--max-chars` to limit how much extracted PDF text is sent to the model.
- Run `--no-llm` first to get a quick draft, then use LLM mode for important papers.
- Add section filtering so only method, experiments, and appendix sections are sent to high-cost agents.
- Cache intermediate agent outputs for repeated runs.
