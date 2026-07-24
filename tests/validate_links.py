"""Check repository-local Markdown links without network access."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

REPOSITORY = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)", re.DOTALL)


for document in REPOSITORY.rglob("*.md"):
    if ".git" in document.parts:
        continue
    text = document.read_text(encoding="utf-8")
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = unquote(target.split("#", 1)[0])
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        if not (document.parent / target).exists():
            relative = document.relative_to(REPOSITORY)
            raise SystemExit(f"{relative}: missing local link target {target}")

print("repository-local Markdown links are valid")
