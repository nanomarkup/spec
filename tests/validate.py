"""Validate Nano Markup conformance manifests without an implementation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
SPECIFICATION = "1.0.0-rc.1"


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
        fail(f"{path.relative_to(REPOSITORY)}: {error}")


def validate_specification_identity() -> None:
    heading = (REPOSITORY / "SPEC.md").read_text(encoding="utf-8").splitlines()[0]
    if heading != f"# Nano Markup {SPECIFICATION}":
        fail("SPEC.md: heading does not match the release specification")
    manifests = (
        ROOT / "manifest.json",
        ROOT / "writer" / "manifest.json",
        ROOT / "byte-integrity.json",
        REPOSITORY / "examples" / "manifest.json",
    )
    for path in manifests:
        manifest = load_json(path)
        if not isinstance(manifest, dict) or manifest.get("specification") != SPECIFICATION:
            fail(f"{path.relative_to(REPOSITORY)}: specification version mismatch")


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


def validate_byte_integrity() -> None:
    manifest = load_json(ROOT / "byte-integrity.json")
    if (
        not isinstance(manifest, dict)
        or manifest.get("manifest_version") != 1
        or manifest.get("algorithm") != "sha256"
        or not isinstance(manifest.get("files"), dict)
    ):
        fail("byte-integrity.json: invalid manifest")
    files = manifest["files"]
    assert isinstance(files, dict)
    protected = {
        fields[0].removeprefix("tests/")
        for line in (REPOSITORY / ".gitattributes").read_text(encoding="utf-8").splitlines()
        if len(fields := line.split()) >= 2 and "-text" in fields[1:]
    }
    if set(files) != protected:
        fail("byte-integrity.json: entries do not match .gitattributes -text paths")
    for relative, expected in files.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            fail("byte-integrity.json: paths and hashes must be strings")
        path = ROOT / relative
        if not path.is_file():
            fail(f"byte-integrity.json: missing {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"byte-integrity.json: checksum mismatch for {relative}")


def validate_examples() -> None:
    root = REPOSITORY / "examples"
    manifest = load_json(root / "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("manifest_version") != 1:
        fail("examples/manifest.json: unsupported manifest version")
    referenced: set[str] = set()
    for case in manifest.get("examples", []):
        for field in ("source", "expected"):
            relative = case[field]
            if relative in referenced or not (root / relative).is_file():
                fail(f"examples/manifest.json: invalid reference {relative}")
            referenced.add(relative)
        if not is_tree(load_json(root / case["expected"])):
            fail(f"examples/{case['expected']}: expected value is not a Nano Markup tree")
    example_files = {
        path.name for path in root.iterdir() if path.suffix in {".nano", ".json"}
    } - {"manifest.json"}
    if example_files != referenced:
        fail("examples/manifest.json does not reference every example exactly once")


validate_specification_identity()
validate_decoder_manifest()
validate_writer_manifest()
validate_byte_integrity()
validate_examples()
print("specification identity, manifests, byte integrity, and examples are valid")
