# Nano Markup 0.1-draft

## 1. Status and conformance

This document is the normative specification for Nano Markup 0.1-draft.
The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are
to be interpreted as requirement levels.

A conforming parser MUST accept every valid conformance fixture, produce the
specified data tree, and reject every invalid fixture with the specified error
category. Exact diagnostic wording is implementation-defined.

## 2. Data model

A Nano Markup value is exactly one of:

- **String**: a sequence of Unicode scalar values.
- **Mapping**: an unordered association of unique keys to values.
- **Sequence**: an ordered collection of values. Values in one sequence MAY
  have different types.

Comments and formatting are not part of the data model. Nano Markup does not
infer nulls, booleans, numbers, dates, or any other scalar types. Applications
MAY interpret strings using rules outside this specification.

## 3. Source text

A document MUST be UTF-8 without a byte-order mark. Invalid UTF-8, NUL, and
literal control characters U+0001 through U+001F other than CR and LF used as
line endings are errors. CRLF and LF line endings are accepted and normalized
to LF before parsing. A final line ending does not add data.

A literal tab is forbidden everywhere, including indentation and scalar text.
The two-character escape `\t` represents a tab in a quoted string.

Whitespace-only lines are blank lines and are ignored except while collecting
a multiline block as described in section 8.

## 4. Indentation

Indentation expresses containment. One indentation level is exactly four ASCII
spaces. Every nonblank line MUST begin with a number of spaces divisible by
four. Tabs, partial levels, skipped levels, and indentation without a parent
container or multiline block are errors.

A child is indented exactly one level more than its parent header. A dedent ends
the current container and returns to the matching earlier level.

## 5. Keys

A key matches this grammar:

```text
[A-Za-z_][A-Za-z0-9_-]*
```

Keys are case-sensitive. Two equal keys MUST NOT occur in the same mapping.
The same key MAY occur in different mappings.

## 6. Documents

An empty document represents an empty mapping.

By default, top-level entries form an implicit mapping. A root sequence is
written as a single `:` header at indentation level zero; all sequence items
are its children. The root `:` MUST be the document's only top-level data
entry. Blank lines and comments MAY appear before or after it.

A document cannot have a scalar root. A quoted line at the root, for example,
is an attempted scalar root and produces `E_SYNTAX` rather than a mapping key.

## 7. Mappings and sequences

### 7.1 Mapping entries

Within a mapping, one data line has one of these forms:

```text
key value    raw or quoted string
key          empty string
key |        multiline string
key..        nested mapping
key:         nested sequence
```

The separator between a key and a scalar or `|` is exactly one ASCII space.
Additional leading or trailing spaces in an unquoted value are errors and must
instead be represented with a quoted string.

`key..` and `key:` contain all immediately following lines indented exactly one
level deeper. With no such data lines they represent empty containers.

### 7.2 Sequence items

Every sequence item begins exactly one level deeper than its sequence header.
An item has one of these forms after indentation is removed:

```text
value    raw or quoted string
|        multiline string
..       nested mapping
:        nested sequence
```

An empty string item MUST be written as `""`. The exact raw strings `..`, `:`,
and `|` MUST be quoted because their unquoted forms are structural markers.
Anonymous mapping and sequence items contain their immediately following lines
indented exactly one further level. With no such data lines they are empty.

## 8. Strings

### 8.1 Raw strings

A raw string is nonempty text on one physical line. It MUST NOT begin or end
with an ASCII space, begin with `"`, or contain a control character. A sequence
raw string also cannot begin with `#`, because that spelling starts a comment.
All other Unicode scalar values are preserved exactly.

On a sequence line, the exact tokens `..`, `:`, and `|` are not raw strings.
On a mapping line, structural markers are recognized only in the complete forms
defined in section 7.1.

### 8.2 Quoted strings

A quoted string begins and ends with `"` and MUST occupy the complete scalar
position. It supports exactly these escapes:

| Escape | Value |
| --- | --- |
| `\"` | quotation mark |
| `\\` | reverse solidus |
| `\n` | line feed |
| `\r` | carriage return |
| `\t` | tab |

Other escapes, missing closing quotes, and unescaped control characters are
errors. Unicode text is written directly as UTF-8; `\u` escapes are not part
of this draft.

### 8.3 Multiline strings

A multiline string begins with `key |` in a mapping or `|` in a sequence. Its
content is collected from following physical lines at least one indentation
level deeper than the header. Exactly one structural indentation level is
removed from every nonblank content line; any additional spaces are preserved.

Blank physical lines encountered while collecting a block become empty content
lines. Trailing empty content lines are discarded. Remaining content lines are
joined with LF, and no terminal LF is added. A block with no nonblank content is
the empty string.

Within a multiline block, mapping, sequence, quote, escape, and comment syntax
has no special meaning. A nonblank line indented at or above the header's level
ends the block and is parsed normally.

## 9. Comments

Outside multiline blocks, a line whose first non-indentation character is `#`
is a comment and is ignored. Inline comments are not supported. A `#` elsewhere
in a raw or quoted scalar is data.

Comment indentation MUST use complete four-space levels, but comments do not
open containers or change the indentation stack.

## 10. Errors

Conformance fixtures use these stable error categories:

- `E_ENCODING`: invalid UTF-8, a byte-order mark, NUL, or forbidden control text.
- `E_TAB`: a literal tab anywhere in the source.
- `E_INDENT`: partial, skipped, mixed, or unexpected indentation.
- `E_KEY`: a key does not match the required grammar.
- `E_DUPLICATE_KEY`: a mapping contains a duplicate key.
- `E_ESCAPE`: an invalid quoted-string escape.
- `E_STRING`: malformed quoted or raw string syntax.
- `E_SYNTAX`: any other structurally invalid document.

If more than one category could apply, a parser MAY report either category
unless a conformance fixture requires one specific category.

## 11. JSON representation used by tests

Expected-result files use JSON only as a language-neutral description of the
Nano Markup data tree:

- a Nano Markup mapping is a JSON object;
- a Nano Markup sequence is a JSON array;
- a Nano Markup string is a JSON string.

This representation does not add JSON typing to Nano Markup. For example,
`age 20` maps to the JSON string `"20"`, not the JSON number `20`.

## 12. Example

```text
universities:
    ..
        name Harvard University
        country USA
        address |
            Massachusetts Hall
            Cambridge, MA 02138
        students:
            ..
                name Mark
                age 20
                contacts..
                    email mark@example.com
                    mobile 12345678
```

The example represents a mapping whose `universities` value is a sequence.
That sequence contains a mapping, and every scalar—including `20`—is a string.

## 13. Deferred features

This draft does not define canonical serialization, schemas, references,
aliases, includes, templates, executable expressions, or application-specific
type conversion. Such features require a later specification revision.
