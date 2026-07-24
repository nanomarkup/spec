# Nano Markup

[![CI](https://github.com/nohainc/nanomarkup.spec/actions/workflows/ci.yml/badge.svg)](https://github.com/nohainc/nanomarkup.spec/actions/workflows/ci.yml)
[![Status: 1.0.0](https://img.shields.io/badge/status-1.0.0-brightgreen)](SPEC.md)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-blue)](LICENSE)

Nano Markup is a minimal, indentation-based format for representing strings,
mappings, and sequences in a form designed to be easy for people to read and
write.

[Read the specification](SPEC.md) · [HTML edition](SPEC.html) ·
[Browse Nano/JSON examples](examples) · [Implement Nano Markup](CONFORMANCE.md)

```nano
..
    name Ariana
    languages:
        Slovak
        English
    address|
        20 Forest Street
        811 01 Bratislava
```

The same value in JSON:

```json
{
  "name": "Ariana",
  "languages": ["Slovak", "English"],
  "address": "20 Forest Street\n811 01 Bratislava"
}
```

## The data model

Nano Markup has exactly three value types:

- **String** — Unicode text, including empty and multiline text.
- **Mapping** — an unordered association of unique string keys to values.
- **Sequence** — an ordered collection of values.

Every leaf value is a string. For example, `true`, `20`, and `null` decode as
the strings `"true"`, `"20"`, and `"null"`; an application may interpret them
according to its own domain model.

A document may contain a String root directly, an explicit Mapping root marked
with `..`, or an explicit Sequence root marked with `:`. Nano Markup files use
the `.nano` extension.

## Syntax at a glance

| Value or construct | Nano Markup form |
| --- | --- |
| Root string | `Plain text` |
| Root mapping | `..` |
| Root sequence | `:` |
| Raw string entry | `name Ariana` |
| Quoted string entry | `name "Ariana"` |
| Nested mapping | `contact..` |
| Nested sequence | `languages:` |
| Multiline string | `address\|` |
| Standalone comment | `# comment` |

Indentation is four ASCII spaces per structural level. Comments occupy their
own lines; a `#` within a value is ordinary string data. See
[SPEC.md](SPEC.md) for the complete grammar, escaping rules, parsing algorithm,
and error precedence.

## Why Nano Markup?

- A deliberately small data model with no implicit scalar types.
- Low-punctuation documents for human-edited structured data.
- Direct representation of multiline text.
- A precise normative specification with deterministic error categories.
- Language-neutral decoder and writer fixtures for interoperability testing.
- Independent implementations that can cross-read one another's output.

Nano Markup can be used for configuration, metadata, small data files, and
other human-edited structured content where its three-type model is a good fit.

## Start here

### Use Nano Markup

- Explore the paired [Nano Markup and JSON examples](examples).
- Use the [Python implementation](https://github.com/nohainc/nanomarkup.python).
- Use the [Go implementation](https://github.com/nohainc/nanomarkup.go).

The implementation repositories document their language-specific APIs,
installation methods, supported specification version, and release status.

### Implement Nano Markup

- Read the normative [Markdown specification](SPEC.md), or its generated,
  informative [HTML rendering](SPEC.html).
- Consult [grammar.ebnf](grammar.ebnf) for a compact lexical summary;
  indentation remains defined normatively by the specification.
- Follow the language-neutral [conformance protocol](CONFORMANCE.md).
- Run the decoder and writer fixtures in [tests](tests).
- Review the [requirement-to-evidence map](tests/REQUIREMENTS.md).

The specification repository intentionally contains no production decoder and
no implementation-specific build system. Each implementation belongs in its
own repository and consumes a pinned version of this conformance suite.
Implementations provide interoperability evidence; they are not normative
dependencies of the language.

### Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a specification change.
[VERSIONING.md](VERSIONING.md) explains compatibility promises, and
[SECURITY.md](SECURITY.md) explains responsible security reporting.

## Release status

The current specification is **Nano Markup 1.0.0**, the first stable release of
the language. Implementations identify the exact specification version and the
decoder or writer profiles they support. Published releases are immutable;
known errors are recorded in [ERRATA.md](ERRATA.md).

Comments and formatting are presentation metadata, not serialized data. A
normal data decoder may discard them; source-preserving editors may expose a
separate document model. The specification defines the applicable round-trip
guarantees.

Canonical serialization, schemas, references, includes, templates, and
executable expressions are outside Nano Markup 1.0.

## Repository guide

| Path | Purpose |
| --- | --- |
| [SPEC.md](SPEC.md) | Normative language specification |
| [SPEC.html](SPEC.html) | Generated informative browser rendering |
| [grammar.ebnf](grammar.ebnf) | Informative lexical grammar summary |
| [examples](examples) | Paired Nano Markup and JSON examples |
| [tests](tests) | Language-neutral conformance fixtures and evidence |
| [CONFORMANCE.md](CONFORMANCE.md) | Decoder and writer adapter protocol |
| [CHANGELOG.md](CHANGELOG.md) | Specification change history |
| [VERSIONING.md](VERSIONING.md) | Draft, RC, and stable compatibility rules |
| [RELEASING.md](RELEASING.md) | Independent specification release procedure |
| [releases](releases) | Release notes and interoperability evidence |
| [ERRATA.md](ERRATA.md) | Known errors in immutable releases |

## Build the HTML specification

`SPEC.md` is the normative source. To regenerate its browser-friendly HTML
rendering:

```console
python -m pip install -r requirements-docs.txt
python tools/render_spec.py
```

CI checks that `SPEC.html` remains synchronized with `SPEC.md`.

## License

Copyright © 2026 Nano Markup contributors.

The specification and conformance material are licensed under the
[Creative Commons Attribution 4.0 International License](LICENSE).
