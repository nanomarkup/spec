# Nano Markup 0.4-draft

## 1. Status and conformance

This document is the normative specification for Nano Markup 0.4-draft.
The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are
to be interpreted as requirement levels.

A conforming data decoder MUST accept every valid conformance fixture, produce
the specified data tree, and reject every invalid fixture with the specified
error category. Exact diagnostic wording is implementation-defined.

A conforming data writer MUST accept a Nano Markup document tree and emit a
Nano Markup document that a conforming decoder reads as a data tree equivalent
to the writer's input. A data writer is not required to reproduce comments,
whitespace, quote choice, line endings, or mapping source order because those
properties are not part of the data model.
A writer given a string root or a value outside the Nano Markup data model MUST
report an error rather than silently alter or omit that value.

An implementation MAY additionally provide a source-preserving document API.
Such an API is outside data conformance and must keep presentation metadata
separate from mapping keys, sequence items, and strings.

The JSON protocol in `CONFORMANCE.md` is test infrastructure, not a Nano Markup
serialization format and not part of the language data model.

## 2. Data model

A Nano Markup value is exactly one of:

- **String**: a sequence of Unicode scalar values excluding U+0000 through
  U+0008, U+000B through U+000C, U+000E through U+001F, and U+007F through
  U+009F. TAB, LF, and CR are permitted string values.
- **Mapping**: an unordered association of unique Nano Markup keys to values.
- **Sequence**: an ordered collection of values. Values in one sequence MAY
  have different types.

A Nano Markup document tree is a Nano Markup value whose root is a Mapping or
Sequence. A String is a value only within a Mapping or Sequence; it cannot be a
document root. Every decoded document and every input accepted by a conforming
data writer is therefore a document tree.

String and key comparison is code-point exact and performs no Unicode
normalization or case folding. Two mappings are equivalent when they contain
the same keys associated with equivalent values, regardless of source order.
Two sequences are equivalent when they have the same number of positionally
equivalent items. Duplicate sequence items are significant and permitted.

Comments, whitespace, quote choice, line endings, and mapping source order are
presentation metadata and are not part of the data model. A data decoder MAY
discard them. Inserting or removing a comment outside a multiline string MUST
NOT change the decoded data tree.

Consequently, data round-tripping and source round-tripping are different:

- `decode(encode(tree))` MUST produce a data tree equivalent to `tree` for
  every Nano Markup document tree accepted by the writer.
- `encode(decode(document))` is not required to reproduce the original source.

Nano Markup does not infer nulls, booleans, numbers, dates, or any other scalar
types. Applications MAY interpret strings using rules outside this
specification.

## 3. Source text

The conventional file extension for a Nano Markup source document is `.nano`.

A document MUST be UTF-8 without a byte-order mark. Invalid UTF-8 and literal
U+0000 through U+0008, U+000B through U+000C, U+000E through U+001F, or U+007F
through U+009F are errors. Literal TAB is handled separately below. Literal CR
and LF are permitted only as physical line endings as defined below.

LF and CRLF are both valid physical line endings and MAY be mixed in one
document. Every CRLF pair is normalized to LF before structural parsing. A CR
not immediately followed by LF is invalid. A final LF or CRLF terminates the
last physical line but does not create an additional blank line or data value.

A conforming writer MUST use either LF or CRLF for every line ending in one
emitted document and SHOULD use LF unless its caller requests CRLF. The selected
source line ending is presentation metadata. Normal data decoding does not
preserve it; a source-preserving document API MAY do so.

A literal tab is forbidden everywhere, including indentation and scalar text.
The two-character escape `\t` represents a tab in a quoted string.

Whitespace-only lines are blank lines and are ignored except while collecting
a multiline block as described in section 8.

## 4. Indentation

Indentation expresses containment. One indentation level is exactly four ASCII
spaces. Every nonblank syntax or comment line MUST begin with a number of
spaces divisible by four. Tabs, partial levels, skipped levels, and syntax
indentation without a parent container or multiline block are errors. A
comment line need not correspond to an open container, because its indentation
is presentation metadata, but its indentation is validated before the comment
is ignored.

After the required structural prefix has been removed, multiline block content
MAY begin with any number of additional ASCII spaces. Those spaces are string
data and do not have to form complete indentation levels.

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
There is no alternate scalar-root spelling.

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
with an ASCII space, begin with `"`, contain a literal TAB, CR, or LF, or
contain a Unicode scalar value excluded by section 2. A sequence raw string
also cannot begin with `#`, because that spelling starts a comment. All other
Unicode scalar values are preserved exactly.

On a sequence line, the exact tokens `..`, `:`, and `|` are not raw strings.
On a mapping line, structural markers are recognized only in the complete forms
defined in section 7.1.

The spellings that require quoting in a scalar position are summarized here:

| Scalar value | Mapping value | Sequence item |
| --- | --- | --- |
| empty string | bare key or `""` | `""` |
| `|` | `"|"` | `"|"` |
| `..` | `..` or `".."` | `".."` |
| `:` | `:` or `":"` | `":"` |
| begins with `#` | raw or quoted | quoted |

In the mapping column, `..` and `:` are values following the required key and
separator; for example, `marker ..`. The forms `key..`, `key:`, and `key |`
remain structural syntax.

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

Other escapes, missing closing quotes, trailing text after the closing quote,
unescaped TAB, CR, or LF, and Unicode scalar values excluded by section 2 are
errors. Unicode text is written directly as UTF-8; `\u` escapes are not part of
this draft.

### 8.3 Multiline strings

A multiline string begins with `key |` in a mapping or `|` in a sequence. Its
content is collected before the following physical lines are interpreted as
comments or structural syntax. A nonblank content line must begin with at least
one indentation level more than the block header. Exactly that required prefix
is removed; every additional character, including spaces and `#`, is preserved.

Blank physical lines encountered while collecting a block become empty content
lines. Their behavior is:

- leading blank lines before the first nonblank content line are preserved;
- blank lines between nonblank content lines are preserved;
- blank lines after the last nonblank content line are discarded;
- a block with no nonblank content is the empty string.

Remaining content lines are joined with LF regardless of whether their source
lines used LF or CRLF. No terminal LF is added automatically. To represent a
string that deliberately ends with LF, use a quoted `\n` escape.

Within a multiline block, mapping, sequence, quote, escape, and comment syntax
has no special meaning. A nonblank line with less than the required content
prefix ends the block and is parsed normally. If that line's indentation is not
valid in the surrounding structure, parsing subsequently produces `E_INDENT`.

## 9. Comments

Outside multiline blocks, a line whose first non-indentation character is `#`
is a comment. A data decoder MUST ignore the entire line, including its line
ending. Inline comments are not supported. A `#` elsewhere in a raw or quoted
scalar is data.

Source encoding, forbidden-character, tab, and indentation validation occurs
before a comment line is ignored. A comment cannot hide an otherwise invalid
byte, character, tab, or partial indentation level.

Comment indentation MUST use complete four-space levels, but comments do not
open containers, close containers, satisfy a container's need for a child,
participate in duplicate-key detection, or add any value to the data tree.
Comments MAY occur before or after the root and between any two syntax lines.

A writer serializing only a data tree SHOULD emit no comments because the tree
contains no comment information. An implementation MAY accept comment metadata
through a separate document API, but that API is not part of Nano Markup data
conformance. A tool claiming source-preserving behavior must retain comments
outside its data tree and restore their relative placement.

Removing every comment line from a valid document MUST leave a document with
the same decoded data tree. This rule does not apply to lines beginning with
`#` inside multiline strings, where the character is data.

### 9.1 Data serialization example

Given this source document:

```text
# User profile
name Ariana
age 12
```

a data decoder produces a mapping equivalent to:

```json
{
  "name": "Ariana",
  "age": "12"
}
```

A data writer may later emit only:

```text
name Ariana
age 12
```

Losing the comment in this operation is expected presentation loss, not data
loss. A source-preserving editor must use a separate document representation.

## 10. Normative parsing algorithm

A conforming decoder MUST behave as if it performs the following steps. It may
use any internal architecture that produces the same result.

### 10.1 Prepare physical lines

1. Decode the input as UTF-8 and reject a byte-order mark, invalid byte
   sequence, U+0000 through U+0008, U+000B through U+000C, U+000E through
   U+001F, or U+007F through U+009F with `E_ENCODING`.
2. Reject a literal tab anywhere with `E_TAB`.
3. Convert every CRLF pair to LF. LF and CRLF may be mixed. A CR not followed
   by LF is `E_ENCODING`.
4. Split the source into physical lines. A final LF terminates the last line but
   does not create an additional blank line.

### 10.2 Classify the root

1. Ignore blank and comment lines while looking for the first data line.
2. If there is no data line, return an empty mapping.
3. If the first data line is exactly `:` at indentation level zero, create a
   root sequence and parse its children at level one. Any other top-level data
   line after that sequence is `E_SYNTAX`.
4. Otherwise, create an implicit root mapping and parse entries at level zero.
   A top-level line that is only a scalar is `E_SYNTAX`.

### 10.3 Parse indentation and containers

For syntax and comment lines, count leading ASCII spaces and require the count
to be divisible by four. The quotient is the indentation level. Blank lines do
not change the current level.

When parsing a mapping or sequence at level `n`:

1. After validating their indentation, ignore blank and comment lines, except
   that multiline collection follows section 10.5.
2. A data line below level `n` ends the current container.
3. A data line above level `n` without a preceding container or multiline
   header at level `n` is `E_INDENT`.
4. A child of a container header at level `n` must be at level `n + 1`.
   Encountering a deeper level is `E_INDENT`; encountering the same or a lower
   level means the container is empty.
5. Mapping keys are compared exactly as written. A repeated key in the current
   mapping is `E_DUPLICATE_KEY`.

Blank and comment lines between a container header and the next data line do
not make the container nonempty. The next data line determines whether a child
exists.

### 10.4 Recognize syntax lines

In a mapping, after indentation is removed, recognize a line in this order:

1. Exact `key..`: nested mapping.
2. Exact `key:`: nested sequence.
3. Exact `key |`: multiline string.
4. Exact `key`: empty string.
5. Exact `key`, one ASCII space, then a raw or quoted scalar.

In a sequence, recognize a line in this order:

1. Exact `..`: mapping item.
2. Exact `:`: sequence item.
3. Exact `|`: multiline string item.
4. A raw or quoted scalar item.

The key and scalar must satisfy sections 5 and 8. Text that matches none of the
forms is an error from the most specific applicable category in section 11.

### 10.5 Collect multiline strings

For a multiline header at level `n`, the required content prefix is exactly
`4 × (n + 1)` ASCII spaces.

1. Visit subsequent physical lines without first classifying comments.
2. Accumulate blank lines provisionally.
3. If a nonblank line begins with the required prefix, remove exactly that
   prefix, append any provisional blank lines, and append the remaining text.
4. If a nonblank line does not begin with the required prefix, discard
   provisional trailing blank lines and end the block before that line.
5. At end-of-file, discard provisional trailing blank lines.
6. Join collected lines with LF and do not append an implicit terminal LF.

After collection ends, resume structural parsing at the first unconsumed line.

### 10.6 Produce the data tree

Decode quoted escapes only after a scalar has been classified as quoted. Keep
raw and multiline content exactly as defined in section 8. Comments and other
presentation metadata are not inserted into the result.

## 11. Errors

Conformance fixtures use these stable error categories:

- `E_ENCODING`: invalid UTF-8, a byte-order mark, a bare CR, or a forbidden
  control character.
- `E_TAB`: a literal tab anywhere in the source.
- `E_INDENT`: partial, skipped, mixed, or unexpected indentation.
- `E_KEY`: a key does not match the required grammar.
- `E_DUPLICATE_KEY`: a mapping contains a duplicate key.
- `E_ESCAPE`: an invalid quoted-string escape.
- `E_STRING`: malformed quoted or raw string syntax.
- `E_SYNTAX`: any other structurally invalid document.

When more than one error exists, a conforming decoder MUST report the category
with the highest priority in this order:

1. `E_ENCODING`
2. `E_TAB`
3. `E_INDENT`
4. `E_SYNTAX`
5. `E_KEY`
6. `E_DUPLICATE_KEY`
7. `E_ESCAPE`
8. `E_STRING`

Within one category, the error whose offending source byte occurs first MUST be
reported. For an error detected at end-of-input, the position immediately after
the final byte is its source position. This ordering makes conformance
deterministic; implementations may still provide additional diagnostics outside
the conformance result.

## 12. JSON representation used by tests

Expected-result files use JSON only as a language-neutral description of the
Nano Markup data tree:

- a Nano Markup mapping is a JSON object;
- a Nano Markup sequence is a JSON array;
- a Nano Markup string is a JSON string.

This representation does not add JSON typing to Nano Markup. For example,
`age 20` maps to the JSON string `"20"`, not the JSON number `20`.

## 13. Example

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

## 14. Deferred features

This draft does not define canonical serialization, schemas, references,
aliases, includes, templates, executable expressions, or application-specific
type conversion. Such features require a later specification revision.

## 15. Security and resource limits

Nano Markup has no executable directives: comments, keys, and values MUST NOT
change parser configuration or invoke code merely by being parsed.

Implementations MAY limit input bytes, line length, nesting depth, mapping or
sequence size, and decoded string size to protect against resource exhaustion.
Limits and the error reported when they are exceeded MUST be documented. A
decoder must apply duplicate-key checks even when processing untrusted input.
