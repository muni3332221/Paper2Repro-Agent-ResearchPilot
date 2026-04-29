# Contributing

Thanks for improving Paper2Repro Agent.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,llm]'
pytest
```

## Guidelines

- Keep generated reproduction code honest: mark uncertain paper-specific details as TODO.
- Add tests for parser, extraction, or reporting changes.
- Avoid hardcoding claims about papers unless they come from parsed text.
