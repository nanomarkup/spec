# Conformance tests

`manifest.json` lists every fixture. Valid `.nano` files have an expected JSON
data tree. Invalid `.nano` files have one required error category from section
11 of `SPEC.md`.

A conforming parser must:

1. Parse every entry in `valid` to a tree deeply equal to its expected JSON.
2. Reject every entry in `invalid` with the listed category.
3. Treat paths as relative to this directory.

Exact diagnostic text, source ranges, and recovery after the first error are
implementation-defined. Byte-sensitive fixtures are intentionally excluded
from Git line-ending normalization.

Expected JSON describes only the data model. Comments, formatting, quote
choice, line endings, and mapping source order never appear in expected output.

Some fixtures intentionally contain CRLF, mixed endings, no final newline,
bare CR, a UTF-8 BOM, invalid UTF-8, forbidden control bytes, or trailing
whitespace. Git text normalization is disabled for those paths. Tools must read
`.nano` fixtures as raw bytes and must not rewrite them merely by opening the
repository.

See [COVERAGE.md](COVERAGE.md) for the rule-to-fixture matrix and
[CONFORMANCE.md](../CONFORMANCE.md) for the decoder adapter protocol.
