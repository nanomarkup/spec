"""Validate metadata that must be finalized before creating a release tag."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent

if len(sys.argv) != 2 or not sys.argv[1].startswith("v"):
    raise SystemExit("usage: validate_release.py vVERSION")

tag = sys.argv[1]
version = tag.removeprefix("v")
heading = (REPOSITORY / "SPEC.md").read_text(encoding="utf-8").splitlines()[0]
if heading != f"# Nano Markup {version}":
    raise SystemExit(f"SPEC.md does not identify {version}")

manifest_paths = (
    "tests/manifest.json",
    "tests/writer/manifest.json",
    "tests/byte-integrity.json",
    "examples/manifest.json",
)
for relative in manifest_paths:
    manifest = json.loads((REPOSITORY / relative).read_text(encoding="utf-8"))
    if manifest.get("specification") != version:
        raise SystemExit(f"{relative} does not identify {version}")

changelog = (REPOSITORY / "CHANGELOG.md").read_text(encoding="utf-8")
release_heading = rf"^## {re.escape(version)} — \d{{4}}-\d{{2}}-\d{{2}}$"
if re.search(release_heading, changelog, re.MULTILINE) is None:
    raise SystemExit(f"CHANGELOG.md has no dated {version} release section")

release_notes = REPOSITORY / "releases" / f"{version}.md"
if not release_notes.is_file():
    raise SystemExit(f"missing releases/{version}.md")
notes_heading = release_notes.read_text(encoding="utf-8").splitlines()[0]
if notes_heading != f"# Nano Markup {version}":
    raise SystemExit(f"releases/{version}.md does not identify {version}")
if "PENDING" in release_notes.read_text(encoding="utf-8"):
    raise SystemExit(f"releases/{version}.md still contains pending evidence")

print(f"release metadata is consistent for {tag}")
