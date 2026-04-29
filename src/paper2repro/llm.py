from __future__ import annotations

import json
import os
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """Small OpenAI wrapper with graceful fallback when the SDK/key is unavailable."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = os.getenv("PAPER2REPRO_MODEL", model)
        self.enabled = bool(os.getenv("OPENAI_API_KEY"))
        self._client: Any | None = None
        if self.enabled:
            try:
                from openai import OpenAI

                self._client = OpenAI()
            except Exception:
                self.enabled = False

    def complete_json(self, system: str, user: str, schema: type[T]) -> T | None:
        if not self.enabled or self._client is None:
            return None
        response = self._client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        data = json.loads(content)
        return schema.model_validate(data)
