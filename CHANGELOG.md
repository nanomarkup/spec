# Changelog

All normative changes to Nano Markup are recorded here.

## 1.0.0-rc.1 — 2026-07-24

- Defined the normative release contents and versioned decoder and writer
  conformance claims independently from implementation repositories.
- Added explicit BCP 14, UTF-8, and Unicode terminology references and a
  version-independent definition of Unicode scalar values.
- Clarified that protocol version 1 transports error categories but not source
  positions, leaving earliest-position verification to native tests and review.
- Clarified that ASCII-space-only physical lines remain blank inside multiline
  blocks and require quoted writer output when their spaces are string data.
- Expanded writer coverage for root strings, space-only logical lines, Unicode
  boundaries, and nested mapping and sequence contexts.
- Expanded decoder coverage for every adjacent error-priority pair, Unicode
  exactness, syntax lookalikes, separator boundaries, and arbitrary comment
  indentation.
- Added explicit fixtures for multiple-level dedents and empty containers
  followed by siblings at different nesting depths.
- Added a normative requirement traceability index and documented native
  writer checks that cannot be represented by the JSON protocol.
- Added byte-sensitive fixture checksums, informative examples, release and
  errata procedures, security reporting guidance, and tag-release automation.
- Updated the conformance documentation to match the shipped runner and writer
  protocol.

## 0.5-draft — 2026-07-23

- Clarified that only empty or ASCII-space-only physical lines are blank;
  permitted Unicode whitespace remains string data in every scalar context.
- Completed the root data model by allowing String, Mapping, and Sequence
  values as document roots.
- Replaced the implicit mapping root with the explicit `..` mapping marker;
  root mapping entries are indented one level beneath it.
- Made mapping-like level-zero text such as `name Ariana` or `colors:` a root
  string; existing mapping documents must add `..` and indent their entries.
- Defined direct raw and quoted root strings plus `|` root multiline strings,
  including empty and reserved-string spellings.
- Expanded and migrated the conformance corpus for explicit roots, root
  strings, sibling rejection, and malformed root indentation.

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
