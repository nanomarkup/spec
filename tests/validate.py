"""Validate Nano Markup conformance manifests without an implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def is_tree(value: object) -> bool:
    if isinstance(value, str):
        return True
    if isinstance(value, list):
        return all(is_tree(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and is_tree(item) for key, item in value.items())
    return False


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"{path.relative_to(ROOT)}: {error}")


def validate_decoder_manifest() -> None:
    manifest = load_json(ROOT / "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("manifest_version") != 1:
        fail("manifest.json: unsupported manifest version")
    referenced: set[str] = set()
    for case in manifest.get("valid", []):
        for field in ("source", "expected"):
            relative = case[field]
            if relative in referenced:
                fail(f"manifest.json: duplicate reference {relative}")
            referenced.add(relative)
            if not (ROOT / relative).is_file():
                fail(f"manifest.json: missing {relative}")
        if not is_tree(load_json(ROOT / case["expected"])):
            fail(f"{case['expected']}: expected value is not a Nano Markup tree")
    errors = {
        "E_ENCODING", "E_TAB", "E_INDENT", "E_SYNTAX", "E_KEY",
        "E_DUPLICATE_KEY", "E_ESCAPE", "E_STRING",
    }
    for case in manifest.get("invalid", []):
        relative = case["source"]
        if relative in referenced:
            fail(f"manifest.json: duplicate reference {relative}")
        referenced.add(relative)
        if not (ROOT / relative).is_file():
            fail(f"manifest.json: missing {relative}")
        if case.get("error") not in errors:
            fail(f"manifest.json: invalid error for {relative}")
    fixtures = {
        str(path.relative_to(ROOT))
        for directory in (ROOT / "valid", ROOT / "invalid")
        for path in directory.iterdir()
        if path.is_file()
    }
    if fixtures != referenced:
        unreferenced = sorted(fixtures - referenced)
        missing = sorted(referenced - fixtures)
        fail(f"manifest.json: unreferenced={unreferenced}, missing={missing}")


def validate_writer_manifest() -> None:
    root = ROOT / "writer"
    manifest = load_json(root / "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("manifest_version") != 1:
        fail("writer/manifest.json: unsupported manifest version")
    referenced: set[str] = set()
    for group in ("round_trip", "invalid"):
        for case in manifest.get(group, []):
            relative = case["value"]
            if relative in referenced or not (root / relative).is_file():
                fail(f"writer/manifest.json: invalid reference {relative}")
            referenced.add(relative)
            value = load_json(root / relative)
            if group == "round_trip" and not is_tree(value):
                fail(f"writer/{relative}: value is not a Nano Markup tree")
            if group == "invalid" and case.get("error") != "E_VALUE":
                fail(f"writer/manifest.json: invalid error for {relative}")
    fixtures = {
        str(path.relative_to(root))
        for directory in (root / "valid", root / "invalid")
        for path in directory.iterdir()
        if path.is_file()
    }
    if fixtures != referenced:
        fail("writer/manifest.json does not reference every writer fixture exactly once")


validate_decoder_manifest()
validate_writer_manifest()
print("conformance manifests are valid")
