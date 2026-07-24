"""Validate Nano Markup conformance manifests without an implementation."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parent
SPECIFICATION = "1.0.0-rc.1"
KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
FORBIDDEN_SCALARS = {
    *range(0x09),
    *range(0x0B, 0x0D),
    *range(0x0E, 0x20),
    *range(0x7F, 0xA0),
}


def fail(message: str) -> NoReturn:
    raise SystemExit(message)


def is_tree(value: object) -> bool:
    if isinstance(value, str):
        return all(
            ord(character) not in FORBIDDEN_SCALARS
            and not 0xD800 <= ord(character) <= 0xDFFF
            for character in value
        )
    if isinstance(value, list):
        return all(is_tree(item) for item in value)
    if isinstance(value, dict):
        return all(KEY.fullmatch(key) and is_tree(item) for key, item in value.items())
    return False


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object member {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> NoReturn:
    raise ValueError(f"non-standard JSON constant {value}")


def load_json(path: Path) -> object:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        fail(f"{path.relative_to(REPOSITORY)}: {error}")


def exact_keys(value: object, expected: set[str], location: str) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != expected:
        fail(f"{location}: expected exactly {sorted(expected)}")
    return value


def case_list(manifest: dict[str, object], field: str, location: str) -> list[object]:
    value = manifest[field]
    if not isinstance(value, list):
        fail(f"{location}: {field} must be an array")
    return value


def referenced_path(root: Path, relative: object, location: str) -> tuple[str, Path]:
    if not isinstance(relative, str):
        fail(f"{location}: path must be a string")
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        fail(f"{location}: path must remain inside its fixture directory")
    return relative, root / candidate


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
        if (
            not isinstance(manifest, dict)
            or manifest.get("specification") != SPECIFICATION
        ):
            fail(f"{path.relative_to(REPOSITORY)}: specification version mismatch")


def validate_decoder_manifest() -> None:
    manifest = exact_keys(
        load_json(ROOT / "manifest.json"),
        {"manifest_version", "specification", "valid", "invalid"},
        "manifest.json",
    )
    if (
        type(manifest.get("manifest_version")) is not int
        or manifest["manifest_version"] != 1
    ):
        fail("manifest.json: unsupported manifest version")
    referenced: set[str] = set()
    for item in case_list(manifest, "valid", "manifest.json"):
        case = exact_keys(item, {"source", "expected"}, "manifest.json valid case")
        for field in ("source", "expected"):
            relative, path = referenced_path(ROOT, case[field], "manifest.json")
            if relative in referenced:
                fail(f"manifest.json: duplicate reference {relative}")
            referenced.add(relative)
            if not path.is_file():
                fail(f"manifest.json: missing {relative}")
        if not is_tree(load_json(ROOT / case["expected"])):
            fail(f"{case['expected']}: expected value is not a Nano Markup tree")
    errors = {
        "E_ENCODING",
        "E_TAB",
        "E_INDENT",
        "E_SYNTAX",
        "E_KEY",
        "E_DUPLICATE_KEY",
        "E_ESCAPE",
        "E_STRING",
    }
    for item in case_list(manifest, "invalid", "manifest.json"):
        case = exact_keys(item, {"source", "error"}, "manifest.json invalid case")
        relative, path = referenced_path(ROOT, case["source"], "manifest.json")
        if relative in referenced:
            fail(f"manifest.json: duplicate reference {relative}")
        referenced.add(relative)
        if not path.is_file():
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
    manifest = exact_keys(
        manifest,
        {"manifest_version", "specification", "round_trip", "invalid"},
        "writer/manifest.json",
    )
    if (
        type(manifest.get("manifest_version")) is not int
        or manifest["manifest_version"] != 1
    ):
        fail("writer/manifest.json: unsupported manifest version")
    referenced: set[str] = set()
    for group in ("round_trip", "invalid"):
        fields = {"value"} if group == "round_trip" else {"value", "error"}
        for item in case_list(manifest, group, "writer/manifest.json"):
            case = exact_keys(item, fields, f"writer/manifest.json {group} case")
            relative, path = referenced_path(
                root, case["value"], "writer/manifest.json"
            )
            if relative in referenced or not path.is_file():
                fail(f"writer/manifest.json: invalid reference {relative}")
            referenced.add(relative)
            value = load_json(path)
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
        fail(
            "writer/manifest.json does not reference every writer fixture exactly once"
        )


def validate_byte_integrity() -> None:
    manifest = exact_keys(
        load_json(ROOT / "byte-integrity.json"),
        {"manifest_version", "specification", "algorithm", "files"},
        "byte-integrity.json",
    )
    if (
        not isinstance(manifest, dict)
        or type(manifest.get("manifest_version")) is not int
        or manifest.get("manifest_version") != 1
        or manifest.get("algorithm") != "sha256"
        or not isinstance(manifest.get("files"), dict)
    ):
        fail("byte-integrity.json: invalid manifest")
    files = manifest["files"]
    assert isinstance(files, dict)
    protected = {
        fields[0].removeprefix("tests/")
        for line in (REPOSITORY / ".gitattributes")
        .read_text(encoding="utf-8")
        .splitlines()
        if len(fields := line.split()) >= 2 and "-text" in fields[1:]
    }
    if not protected <= set(files):
        fail("byte-integrity.json: missing a .gitattributes -text path")
    for relative, expected in files.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            fail("byte-integrity.json: paths and hashes must be strings")
        relative, path = referenced_path(ROOT, relative, "byte-integrity.json")
        if not SHA256.fullmatch(expected):
            fail(f"byte-integrity.json: invalid SHA-256 digest for {relative}")
        if not path.is_file():
            fail(f"byte-integrity.json: missing {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"byte-integrity.json: checksum mismatch for {relative}")


def validate_examples() -> None:
    root = REPOSITORY / "examples"
    manifest = load_json(root / "manifest.json")
    manifest = exact_keys(
        manifest,
        {"manifest_version", "specification", "examples"},
        "examples/manifest.json",
    )
    if (
        type(manifest.get("manifest_version")) is not int
        or manifest["manifest_version"] != 1
    ):
        fail("examples/manifest.json: unsupported manifest version")
    referenced: set[str] = set()
    for item in case_list(manifest, "examples", "examples/manifest.json"):
        case = exact_keys(item, {"source", "expected"}, "examples manifest case")
        for field in ("source", "expected"):
            relative, path = referenced_path(
                root, case[field], "examples/manifest.json"
            )
            if relative in referenced or not path.is_file():
                fail(f"examples/manifest.json: invalid reference {relative}")
            referenced.add(relative)
        if not is_tree(load_json(root / case["expected"])):
            fail(
                f"examples/{case['expected']}: expected value is not a Nano Markup tree"
            )
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
