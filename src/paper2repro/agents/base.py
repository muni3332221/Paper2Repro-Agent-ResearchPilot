from __future__ import annotations

from dataclasses import dataclass

from paper2repro.llm import LLMClient


@dataclass
class AgentContext:
    llm: LLMClient
    use_llm: bool = True
