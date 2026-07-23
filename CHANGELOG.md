# Changelog

All normative changes to Nano Markup are recorded here.

## 0.2-draft — 2026-07-23

- Defined comments and formatting as presentation metadata outside the data
  model, including the guarantees for data and source round-tripping.
- Added a normative parsing algorithm and syntax-recognition precedence.
- Clarified that multiline block content is collected before comment and
  structural-line recognition.
- Defined `.nano` as the source file extension.
- Added security and resource-limit guidance.
- Expanded conformance coverage for comments, empty documents, empty
  containers containing comments, and multiline content indentation.

## 0.1-draft — 2026-07-23

- Defined strings, mappings, and sequences as the complete data model.
- Defined implicit mapping and explicit sequence document roots.
- Defined four-space indentation and deterministic container markers.
- Added raw, quoted, empty, and explicit multiline strings.
- Defined comments, key uniqueness, source encoding, and error categories.
- Added the first language-neutral conformance fixtures.
