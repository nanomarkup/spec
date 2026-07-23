# Changelog

All normative changes to Nano Markup are recorded here.

## 0.4-draft — 2026-07-23

- Distinguished the complete value model from document trees, whose roots are
  restricted to mappings and sequences.
- Defined the complete forbidden-control ranges, including DEL and C1 control
  characters, while retaining escaped TAB, LF, and CR as string values.
- Made error-category selection deterministic and required validation before
  comment lines are discarded.
- Documented reserved scalar spellings and added fixtures for empty roots,
  sequence order and duplicates, key grammar and scope, malformed strings,
  literal tabs, and control characters.

## 0.3-draft — 2026-07-23

- Explicitly accepted LF, CRLF, and mixed LF/CRLF source documents while
  continuing to reject bare CR.
- Defined writer line-ending behavior and multiline normalization to LF.
- Finalized leading, internal, and trailing blank-line behavior for multiline
  strings and expanded multiline edge fixtures.
- Added byte-level fixtures for BOM, invalid UTF-8, forbidden controls, and
  bare CR.
- Added a conformance coverage matrix and language-neutral JSON adapter
  protocol.
- Kept production decoders and CI outside the specification repository.

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
