# Nano Markup examples

These examples are informative introductions to each root value shape. Each
`.nano` document has a neighboring `.json` file describing its decoded Nano
Markup tree through the language-neutral test representation.

- `profile.nano` is a mapping with scalar, multiline, and nested values.
- `colors.nano` is a sequence of strings.
- `root-string.nano` is a direct String root.

The release validator checks that the example manifest is complete and that
every expected JSON file contains only Nano Markup data-model types. The
language-neutral conformance runner also decodes every example with each
supplied adapter. Examples remain informative; normative behavior comes from
`SPEC.md` and the conformance fixtures.
