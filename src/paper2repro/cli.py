from __future__ import annotations

from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from .models import RunConfig
from .pipeline import run_pipeline

app = typer.Typer(help="Turn research papers into reproducible experiment plans.")
console = Console()


@app.command()
def run(
    pdf: Path = typer.Argument(..., exists=True, readable=True, help="Path to the paper PDF."),
    output: Path = typer.Option(Path("outputs"), "--output", "-o", help="Output directory."),
    model: str = typer.Option("gpt-4o-mini", "--model", help="LLM model name."),
    no_llm: bool = typer.Option(False, "--no-llm", help="Disable LLM calls and use heuristic extraction."),
    max_chars: int = typer.Option(50000, "--max-chars", help="Maximum paper text characters to process."),
) -> None:
    """Generate a reproduction plan and starter project from a PDF."""
    load_dotenv()
    config = RunConfig(pdf_path=pdf, output_dir=output, use_llm=not no_llm, model=model, max_chars=max_chars)
    plan = run_pipeline(config)
    console.print(
        Panel.fit(
            f"[bold green]Done[/bold green]\n"
            f"Report: {output / 'repro_plan.md'}\n"
            f"JSON: {output / 'repro_plan.json'}\n"
            f"Starter project: {output / 'starter_project'}\n\n"
            f"Detected framework: {plan.code_plan.framework}",
            title="Paper2Repro Agent",
        )
    )


if __name__ == "__main__":
    app()
