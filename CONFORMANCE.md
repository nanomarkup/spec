# Nano Markup decoder conformance protocol

## Status

This document defines protocol version 1 for testing a Nano Markup decoder
against the `0.5-draft` fixture corpus. It is language-neutral test
infrastructure. JSON is used only to transport test results; it is not part of
Nano Markup syntax or its public data format.

Production decoders belong in separate implementation repositories. An
implementation should pin the specification repository to a tag or commit and
must not modify the shared fixtures to make its own tests pass.

The 0.5-draft defines this contract but does not ship a decoder, runner, or CI
workflow. Those may be added after an independent implementation exercises the
protocol.

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

## Runner behavior

For every `valid` manifest entry, the runner must require `ok: true` and compare
`value` deeply with the referenced expected JSON. Mapping order does not affect
comparison; sequence order and duplicate items do.

For every `invalid` entry, the runner must require `ok: false` and compare the
reported category with `error` in the manifest. A crash or protocol violation
never counts as correctly rejecting a fixture.

The runner must impose a documented timeout and must not allow an adapter to
modify fixtures. Exact diagnostics, source ranges, and recovery after the first
language error remain implementation-defined.

## Writers

Protocol version 1 tests decoders only. Writer conformance will use a separate
round-trip protocol so parser correctness is not confused with formatting,
mapping order, comment preservation, or quote selection.
