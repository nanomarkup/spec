# Nano Markup Specification

This repository contains the official language specification and conformance
tests for Nano Markup, a minimal, human-readable structured data format.

## Status

The current specification is **Nano Markup 1.0.0-rc.1**, the first release
candidate for Nano Markup 1.0. Release-candidate implementations may claim the
exact RC version and conformance profiles they support, but must not describe
themselves as conforming to the final stable 1.0 standard.

Nano Markup source files use the `.nano` extension.

A document may contain a String root directly, an explicit Mapping root marked
with `..`, or an explicit Sequence root marked with `:`.

## Repository contents

- [SPEC.md](SPEC.md) is the normative language specification.
- [grammar.ebnf](grammar.ebnf) summarizes the lexical grammar. Indentation is
  defined normatively in `SPEC.md`.
- [tests](tests) contains valid and invalid conformance fixtures.
- [CONFORMANCE.md](CONFORMANCE.md) defines the language-neutral JSON adapter
  protocol used to test independent decoders.
- [tests/COVERAGE.md](tests/COVERAGE.md) maps normative behavior to fixtures.
- [tests/REQUIREMENTS.md](tests/REQUIREMENTS.md) traces every normative
  requirement to conformance evidence or implementation review.
- [examples](examples) contains informative documents for each root shape.
- [CHANGELOG.md](CHANGELOG.md) records specification changes.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to propose changes.
- [VERSIONING.md](VERSIONING.md) defines draft, release-candidate, and stable
  compatibility rules.
- [RELEASING.md](RELEASING.md) defines the independent specification release
  procedure.
- [ERRATA.md](ERRATA.md) records known errors in immutable releases.
- [releases](releases) contains reviewed release notes and interoperability
  evidence.
- [SECURITY.md](SECURITY.md) explains responsible security reporting.

Comments and formatting are presentation metadata, not serialized data. A
normal data decoder may discard them; source-preserving editors may expose a
separate document model. See the specification for the round-trip guarantees.

Canonical serialization, schemas, references, includes, templates, and
executable expressions are outside Nano Markup 1.0.

The specification repository intentionally contains no production decoder and
no implementation-specific build system. Each language implementation belongs
in its own repository and consumes a pinned version of this conformance suite.
Implementations are interoperability evidence, not normative dependencies of
the specification.

## License

Copyright © 2026 Nano Markup contributors.

The specification and conformance material are licensed under the
[Creative Commons Attribution 4.0 International License](LICENSE).
