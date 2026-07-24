"""Run decoder/writer protocols and cross-read every writer output."""

from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 5


def fixture_hashes() -> dict[Path, str]:
    normative = {
        path: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in ROOT.rglob("*")
        if path.is_file() and path.suffix in {".nano", ".json"}
    }
    examples = ROOT.parent / "examples"
    normative.update(
        {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in examples.iterdir()
            if path.is_file() and path.suffix in {".nano", ".json"}
        }
    )
    return normative


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object member {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant {value}")


def invoke(command: list[str], *arguments: str) -> dict[str, object]:
    result = subprocess.run(
        [*command, *arguments],
        check=False,
        capture_output=True,
        timeout=TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        diagnostics = result.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"adapter failed: {diagnostics}")
    try:
        output = result.stdout.decode("utf-8")
        if not output.endswith("\n"):
            raise ValueError("result is not terminated by LF")
        body = output[:-1]
        decoder = json.JSONDecoder(
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
        payload, end = decoder.raw_decode(body)
        if end != len(body):
            raise ValueError("bytes follow the JSON object before the final LF")
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise SystemExit(f"adapter returned invalid framed JSON: {error}") from None
    if not isinstance(payload, dict):
        raise SystemExit("adapter result is not an object")
    return payload


def run(adapters: list[list[str]]) -> None:
    decoder_manifest = json.loads((ROOT / "manifest.json").read_text())
    for adapter in adapters:
        for case in decoder_manifest["valid"]:
            expected = json.loads((ROOT / case["expected"]).read_text())
            payload = invoke(adapter, "parse", str(ROOT / case["source"]))
            if payload != {"ok": True, "value": expected}:
                raise SystemExit(f"decoder mismatch for {case['source']}: {payload}")
        for case in decoder_manifest["invalid"]:
            payload = invoke(adapter, "parse", str(ROOT / case["source"]))
            if payload != {"ok": False, "error": case["error"]}:
                raise SystemExit(f"decoder mismatch for {case['source']}: {payload}")

        examples_root = ROOT.parent / "examples"
        examples_manifest = json.loads((examples_root / "manifest.json").read_text())
        for case in examples_manifest["examples"]:
            expected = json.loads((examples_root / case["expected"]).read_text())
            payload = invoke(adapter, "parse", str(examples_root / case["source"]))
            if payload != {"ok": True, "value": expected}:
                raise SystemExit(f"example mismatch for {case['source']}: {payload}")

    writer_root = ROOT / "writer"
    writer_manifest = json.loads((writer_root / "manifest.json").read_text())
    for writer in adapters:
        for case in writer_manifest["round_trip"]:
            expected = json.loads((writer_root / case["value"]).read_text())
            for newline_name in ("LF", "CRLF"):
                payload = invoke(
                    writer, "write", str(writer_root / case["value"]), newline_name
                )
                if set(payload) != {"ok", "source"} or payload["ok"] is not True:
                    raise SystemExit(f"writer failed for {case['value']}: {payload}")
                source = payload["source"]
                if not isinstance(source, str) or "\t" in source:
                    raise SystemExit(
                        "writer emitted a non-string source or literal tab"
                    )
                if newline_name == "LF" and "\r" in source:
                    raise SystemExit("LF writer emitted CR")
                if newline_name == "CRLF":
                    remainder = source.replace("\r\n", "")
                    if "\r" in remainder or "\n" in remainder:
                        raise SystemExit(
                            "CRLF writer emitted an inconsistent line ending"
                        )
                with tempfile.NamedTemporaryFile(suffix=".nano") as temporary:
                    temporary.write(source.encode())
                    temporary.flush()
                    for decoder in adapters:
                        decoded = invoke(decoder, "parse", temporary.name)
                        if decoded != {"ok": True, "value": expected}:
                            raise SystemExit(
                                f"cross-read mismatch for {case['value']}: {decoded}"
                            )
        for case in writer_manifest["invalid"]:
            payload = invoke(writer, "write", str(writer_root / case["value"]), "LF")
            if payload != {"ok": False, "error": case["error"]}:
                raise SystemExit(f"writer accepted {case['value']}: {payload}")
    print(
        f"{len(adapters)} adapters passed decoder, writer, and cross-read conformance"
    )


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: run_conformance.py 'ADAPTER COMMAND'...")
    original_hashes = fixture_hashes()
    try:
        run([shlex.split(argument) for argument in sys.argv[1:]])
    except subprocess.TimeoutExpired as error:
        raise SystemExit(
            f"adapter timed out after {TIMEOUT_SECONDS} seconds: {error.cmd}"
        ) from None
    finally:
        if fixture_hashes() != original_hashes:
            raise SystemExit("an adapter modified a conformance fixture or example")


main()
