# Nano Markup conformance protocol

## Status

This document defines protocol version 1 for testing Nano Markup decoders and writers
against the `1.0.0` fixture corpus. It is language-neutral test
infrastructure. JSON is used only to transport test results; it is not part of
Nano Markup syntax or its public data format.

Protocol version 1 supports the decoder and writer conformance profiles. A
conformance claim identifies the exact Nano Markup specification version and
the profiles exercised. The specification version in both manifests must
match the claimed version. The protocol and its JSON result shapes are
normative for reporting fixture results; they do not define language syntax or
an implementation's public API.

Production decoders belong in separate implementation repositories. An
implementation should pin the specification repository to a tag or commit and
must not modify the shared fixtures to make its own tests pass.

The specification repository ships a language-neutral runner and CI integrity
checks but no production decoder. Independent implementations exercise the
protocol by supplying their adapters to `tests/run_conformance.py`.
The supplied runner also requires every `nano` fenced example in `SPEC.md` to
decode successfully. Fences labeled `nano-invalid` are explanatory malformed
examples and are excluded because their required categories remain covered by
normative fixtures.

## Adapter invocation

A conformance runner invokes an implementation-specific adapter as:

```text
ADAPTER parse PATH
```

`PATH` identifies one `.nano` fixture. The adapter must read the file as raw
bytes so encoding errors are reported by the Nano Markup decoder rather than by
the adapter's host-language text reader.

The adapter must write exactly one UTF-8 JSON object followed by LF to standard
output. Human-readable diagnostics may be written to standard error.

Exit status `0` means the adapter successfully reported either a decoded value
or an expected language error. A nonzero status means the adapter itself could
not run, crashed, timed out, or violated the protocol.

## Successful result

```json
{
  "ok": true,
  "value": {
    "name": "Ariana"
  }
}
```

`value` must recursively contain only JSON objects, arrays, and strings:

- Nano Markup mapping → JSON object
- Nano Markup sequence → JSON array
- Nano Markup string → JSON string

JSON numbers, booleans, and null are protocol violations. JSON object member
order is ignored when results are compared. A top-level JSON string represents
a Nano Markup String root.

## Language-error result

```json
{
  "ok": false,
  "error": "E_INDENT"
}
```

`error` must be one of the categories defined by the pinned specification.
Additional fields are not permitted in protocol version 1, ensuring that test
results remain comparable across implementation languages.

The protocol reports only an error category. The specification's rule for
choosing the earliest error within one category therefore requires native
implementation testing or review in protocol version 1; an adapter cannot
demonstrate it by adding a position field because additional fields are a
protocol violation.

## Runner behavior

For every `valid` manifest entry, the runner must require `ok: true` and compare
`value` deeply with the referenced expected JSON. Mapping order does not affect
comparison; sequence order and duplicate items do.

For every `invalid` entry, the runner must require `ok: false` and compare the
reported category with `error` in the manifest. A crash or protocol violation
never counts as correctly rejecting a fixture.

The supplied runner imposes a five-second timeout on each adapter invocation.
It records every normative fixture and informative example before invoking an
adapter and fails if any of them changes. Operating-system sandboxing is
recommended when running an untrusted adapter. Exact diagnostics, source
ranges, and recovery after the first language error remain
implementation-defined.

## Writers

Writer protocol version 1 invokes an implementation-specific adapter as:

```text
ADAPTER write PATH NEWLINE
```

`PATH` is a UTF-8 JSON file containing only objects, arrays, and strings.
`NEWLINE` is `LF` or `CRLF`. The adapter must write exactly one UTF-8 JSON
object followed by LF. On success it has this shape:

```json
{"ok": true, "source": "..\n    name Ariana"}
```

The runner decodes `source` with every conforming decoder, requires a tree
equivalent to the JSON input, requires the requested physical line ending, and
rejects literal tabs or inconsistent line endings. A writer MAY terminate its
final physical line with the selected line ending. On an input outside the Nano Markup data model the adapter reports
`{"ok": false, "error": "E_VALUE"}`. Protocol error names are test
infrastructure and do not alter implementation-specific public exceptions.

`tests/writer/manifest.json` lists round-trip and invalid writer inputs. JSON
cannot represent cyclic containers or implementation-specific host values, so
each implementation must test those cases in its native suite.

## Manifest schemas

All manifests are UTF-8 JSON objects. Unknown fields are forbidden so a typo
cannot silently weaken the corpus. Object-member names must be unique, and
JSON `NaN`, `Infinity`, and `-Infinity` extensions are forbidden.

`tests/manifest.json` contains exactly `manifest_version`, `specification`,
`valid`, and `invalid`. Each `valid` item contains exactly `source` and
`expected`; each `invalid` item contains exactly `source` and `error`.

`tests/writer/manifest.json` contains exactly `manifest_version`,
`specification`, `round_trip`, and `invalid`. Each `round_trip` item contains
exactly `value`; each `invalid` item contains exactly `value` and `error`.

`examples/manifest.json` contains exactly `manifest_version`, `specification`,
and `examples`. Each example contains exactly `source` and `expected`.

`tests/byte-integrity.json` contains exactly `manifest_version`,
`specification`, `algorithm`, and `files`. `algorithm` is `sha256`; `files` is
an object from repository-relative fixture paths to lowercase hexadecimal
SHA-256 digests. It must include every path marked `-text` in `.gitattributes`
and may also protect other byte-sensitive fixtures.
