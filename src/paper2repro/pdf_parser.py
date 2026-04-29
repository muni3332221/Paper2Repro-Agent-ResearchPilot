from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from .models import PaperDocument, PaperSection

SECTION_PATTERN = re.compile(
    r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?(abstract|introduction|related work|background|method|methods|methodology|approach|experiments?|results|discussion|conclusion|references)\s*$"
)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF with pypdf."""
    reader = PdfReader(str(pdf_path))
    parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def infer_title(text: str, fallback: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    candidates = [line for line in lines[:30] if 5 <= len(line) <= 180]
    for line in candidates:
        lower = line.lower()
        if not any(x in lower for x in ["arxiv", "proceedings", "conference", "abstract"]):
            return line
    return fallback


def split_sections(text: str) -> list[PaperSection]:
    matches = list(SECTION_PATTERN.finditer(text))
    if not matches:
        return [PaperSection(title="Full Text", content=text[:20000])]

    sections: list[PaperSection] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = match.group(1).title()
        content = text[start:end].strip()
        if content:
            sections.append(PaperSection(title=title, content=content[:12000]))
    return sections


def parse_pdf(pdf_path: Path, max_chars: int = 50000) -> PaperDocument:
    text = extract_text_from_pdf(pdf_path)
    compact = re.sub(r"\n{3,}", "\n\n", text).strip()[:max_chars]
    sections = split_sections(compact)
    abstract = ""
    for section in sections:
        if section.title.lower() == "abstract":
            abstract = section.content[:2500]
            break
    return PaperDocument(
        source_path=str(pdf_path),
        title=infer_title(compact, pdf_path.stem),
        abstract=abstract,
        sections=sections,
        raw_text=compact,
    )
