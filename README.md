# Nano Markup Specification

This repository contains the official language specification and conformance
tests for Nano Markup, a minimal, human-readable structured data format.

## Status

The current specification is **Nano Markup 0.1-draft**. It is unstable and may
change incompatibly before version 1.0. Implementations may experiment with the
draft, but must not describe themselves as conforming to a stable Nano Markup
standard.

## Repository contents

- [SPEC.md](SPEC.md) is the normative language specification.
- [grammar.ebnf](grammar.ebnf) summarizes the lexical grammar. Indentation is
  defined normatively in `SPEC.md`.
- [tests](tests) contains valid and invalid conformance fixtures.
- [CHANGELOG.md](CHANGELOG.md) records specification changes.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to propose changes.

Canonical serialization, schemas, references, includes, templates, and
executable expressions are not part of this draft.

## License

Copyright © 2026 Nano Markup contributors.

The specification and conformance material are licensed under the
[Creative Commons Attribution 4.0 International License](LICENSE).
