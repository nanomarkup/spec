"""Run decoder/writer protocols and cross-read every writer output."""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def invoke(command: list[str], *arguments: str) -> dict[str, object]:
    result = subprocess.run(
        [*command, *arguments],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise SystemExit(f"adapter failed: {result.stderr.strip()}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit(f"adapter returned invalid JSON: {error}") from None
    if not isinstance(payload, dict):
        raise SystemExit("adapter result is not an object")
    return payload


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: run_conformance.py 'ADAPTER COMMAND'...")
    adapters = [shlex.split(argument) for argument in sys.argv[1:]]
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
                if not isinstance(source, str) or source.endswith(("\n", "\r")):
                    raise SystemExit("writer emitted an invalid terminal line ending")
                if newline_name == "LF" and "\r" in source:
                    raise SystemExit("LF writer emitted CR")
                if newline_name == "CRLF" and "\n" in source.replace("\r\n", ""):
                    raise SystemExit("CRLF writer emitted a bare LF")
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
    print(f"{len(adapters)} adapters passed decoder, writer, and cross-read conformance")


main()
