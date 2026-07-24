# Nano Markup 1.0.0

## 1. Status and conformance

This document is the normative language specification for Nano Markup
1.0.0. The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and
**MAY** are to be interpreted as described in BCP 14, RFC 2119 and RFC 8174,
when, and only when, they appear in all capitals.

One released specification version consists of the files at one immutable Git
tag. `SPEC.md`, `tests/manifest.json`, `tests/writer/manifest.json`, and every
fixture referenced by those manifests are normative. `CONFORMANCE.md` defines
the normative adapter protocol used to present conformance results, but JSON
transport in that protocol is not Nano Markup syntax. `grammar.ebnf`, examples,
coverage indexes, `SPEC.html`, and explanatory repository documents are
informative. If an informative file conflicts with normative material, the
normative material controls.

Code examples and explanatory notes inside this document illustrate the
normative rules. If an example conflicts with a normative requirement, the
normative requirement controls.

A conforming data decoder MUST implement this specification, accept every
valid conformance fixture, produce the specified data tree, and reject every
invalid fixture with the specified error category. Exact diagnostic wording is
implementation-defined.

A conforming data writer MUST accept a Nano Markup document tree and emit a
Nano Markup document that a conforming decoder reads as a data tree equivalent
to the writer's input. A data writer is not required to reproduce comments,
whitespace, quote choice, line endings, or mapping source order because those
properties are not part of the data model.
A writer given a value outside the Nano Markup data model MUST report an error
rather than silently alter or omit that value.

Conformance is claimed separately for the **decoder** and **writer** profiles.
An implementation may claim either profile or both, but a claim MUST identify
the exact specification version and every claimed profile. For example:
`Nano Markup 1.0.0 decoder and writer`. Partial support within a claimed
profile is not conforming. Passing the shared fixtures is required but does not
replace compliance with normative behavior for inputs not enumerated by the
finite corpus.

An implementation MAY additionally provide a source-preserving document API.
Such an API is outside data conformance and must keep presentation metadata
separate from mapping keys, sequence items, and strings.

The JSON protocol in `CONFORMANCE.md` is conformance test infrastructure, not a
Nano Markup serialization format and not part of the language data model.

## 2. Data model

A Nano Markup value is exactly one of:

- **String**: a sequence of Unicode scalar values excluding U+0000 through
  U+0008, U+000B through U+000C, U+000E through U+001F, and U+007F through
  U+009F. TAB, LF, and CR are permitted string values.
- **Mapping**: an unordered association of unique Nano Markup keys to values.
- **Sequence**: an ordered collection of values. Values in one sequence MAY
  have different types.

A Nano Markup document tree is a finite, acyclic tree of Nano Markup values.
Its root MAY therefore be a String, Mapping, or Sequence. Reusing the same
host-language container in multiple positions is permitted when it does not
form a cycle; Nano Markup defines values, not object identity or references.

For this specification, a Unicode scalar value is an integer from U+0000
through U+10FFFF other than the surrogate range U+D800 through U+DFFF.
Assigned characters, unassigned scalar values, private-use characters, and
noncharacters are treated alike unless excluded explicitly above. Nano Markup
does not depend on Unicode normalization, character properties, or the set of
characters assigned by a particular Unicode version.

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
  every Nano Markup value accepted by the writer.
- `encode(decode(document))` is not required to reproduce the original source.

Nano Markup does not infer nulls, booleans, numbers, dates, or any other scalar
types. Applications MAY interpret strings using rules outside this
specification.

For example, every leaf below is a String, including `true` and `12`:

```nano
..
    enabled true
    age 12
    labels:
        student
        cyclist
```

## 3. Source text

The conventional file extension for a Nano Markup source document is `.nano`.

A document MUST be UTF-8 without a leading byte-order mark (the UTF-8 signature
bytes EF BB BF). U+FEFF appearing after the first source byte is ordinary
string data. Invalid UTF-8 and literal
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

A blank line contains zero or more ASCII spaces and no other characters. Blank
lines are ignored except while collecting a multiline block as described in
section 8. Other Unicode whitespace characters permitted by the data model are
string data, not blank-line syntax.

## 4. Indentation

Indentation expresses containment. One indentation level is exactly four ASCII
spaces. Every nonblank syntax or comment line MUST begin with a number of
spaces divisible by four. Tabs, partial levels, skipped levels, and syntax
indentation without a parent container or multiline block are errors. A
comment line need not correspond to an open container, because its indentation
is presentation metadata, but its indentation is validated before the comment
is ignored.

After the required structural prefix has been removed, a nonblank multiline
content line MAY begin with any number of additional ASCII spaces. Those spaces
are string data and do not have to form complete indentation levels. A physical
line containing only ASCII spaces remains a blank line regardless of its width;
a writer MUST use quoted syntax when a string contains a logical line made only
of spaces.

A child is indented exactly one level more than its parent header. A dedent ends
the current container and returns to the matching earlier level.

Here `child` is eight spaces from the left margin because it is inside
`parent`; the dedented `sibling` returns to the root mapping:

```nano
..
    parent..
        child value
    sibling value
```

## 5. Keys

A key matches this grammar:

```text
[A-Za-z_][A-Za-z0-9_-]*
```

Keys are case-sensitive. Two equal keys MUST NOT occur in the same mapping.
The same key MAY occur in different mappings.

For example, `user_name`, `release-1`, and `Case` are valid and distinct keys.
`1user` and `full name` are not valid keys.

## 6. Documents

An empty document represents an empty mapping.

After blank and comment lines are ignored, a document root has exactly one of
these forms at indentation level zero:

```text
..             mapping; entries are children at level one
:              sequence; items are children at level one
raw string     one-line string
"quoted"       one-line quoted string
|              multiline string; content begins at level one
```

The root value is the document's only top-level data entry. Blank lines and
comments MAY appear before or after it. Any additional top-level data line is
`E_SYNTAX`.

An empty, ASCII-space-only, or comment-only document represents an empty
mapping. Consequently, an empty root string MUST be written as `""`. The exact
root strings `..`, `:`, and `|`, and a root string beginning with `#`, MUST be
quoted because their unquoted forms are structural syntax or a comment.

The root markers follow the anonymous container and multiline markers already
used in sequences. A root mapping or sequence with no child data lines is
empty. Comments do not make it nonempty.

These are three complete documents with different root types:

```nano
Hello from a String root
```

```nano
:
    red
    green
```

```nano
..
    name Ariana
```

Only the exact tokens `..`, `:`, and `|` are recognized as root markers. For
example, `colors:` and `name Ariana` at level zero are raw root strings, not
mapping entries. A mapping containing a named sequence is written explicitly:

```text
..
    colors:
        red
        green
```

## 7. Mappings and sequences

### 7.1 Mapping entries

Within a mapping, one data line has one of these forms:

```text
key value    raw or quoted string
key          empty string
key|         multiline string
key..        nested mapping
key:         nested sequence
```

The separator between a key and a scalar is exactly one ASCII space.
`key|`, like `key..` and `key:`, has no separator before its structural marker.
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

Attached markers create structures, while the same markers after one separator
space are ordinary string values:

```nano
..
    child..
    items:
    description|
        Multiple lines
        of text
    mapping_text ..
    sequence_text :
    pipe_text |
```

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

| Scalar value | Document root | Mapping value | Sequence item |
| --- | --- | --- | --- |
| empty string | `""` | bare key or `""` | `""` |
| `\|` | `"\|"` | `\|` or `"\|"` | `"\|"` |
| `..` | `".."` | `..` or `".."` | `".."` |
| `:` | `":"` | `:` or `":"` | `":"` |
| begins with `#` | quoted | raw or quoted | quoted |

In the mapping column, `..` and `:` are values following the required key and
separator; for example, `marker ..`. The forms `key..`, `key:`, and `key|`
remain structural syntax. At the document root, `..`, `:`, and `|` are also
structural and MUST be quoted when intended as strings.

Raw mapping values may contain spaces and `#`; there is no inline-comment
syntax:

```nano
..
    title Nano Markup language
    note # this complete remainder is string data
```

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
Nano Markup 1.0.

Quoted strings represent otherwise ambiguous whitespace and escaped control
characters:

```nano
..
    padded "  spaces are preserved  "
    lines "first\nsecond"
    tab "left\tright"
```

### 8.3 Multiline strings

A multiline string begins with `key|` in a mapping or `|` at the document root
or in a sequence. Its content is collected before the following physical lines
are interpreted as comments or structural syntax. A nonblank content line must
begin with at least one indentation level more than the block header. Exactly
that required prefix is removed; every additional character, including spaces
and `#`, is preserved.

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

For example, this value decodes to
`"20 Forest Street\n811 01 Bratislava"` without an implicit final LF:

```nano
..
    address|
        20 Forest Street
        811 01 Bratislava
```

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
..
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
..
    name Ariana
    age 12
```

Losing the comment in this operation is expected presentation loss, not data
loss. A source-preserving editor must use a separate document representation.

## 10. Normative parsing algorithm

A conforming decoder MUST behave as if it performs the following steps. It may
use any internal architecture that produces the same result.

### 10.1 Prepare physical lines

1. Decode the input as UTF-8 and reject a leading UTF-8 signature, invalid byte
   sequence, U+0000 through U+0008, U+000B through U+000C, U+000E through
   U+001F, or U+007F through U+009F with `E_ENCODING`.
2. Reject a literal tab anywhere with `E_TAB`.
3. Convert every CRLF pair to LF. LF and CRLF may be mixed. A CR not followed
   by LF is `E_ENCODING`.
4. Split the source into physical lines. A final LF terminates the last line but
   does not create an additional blank line.

### 10.2 Classify the root

1. Validate indentation on comment lines, then ignore blank and comment lines
   while looking for the first data line.
2. If there is no data line, return an empty mapping.
3. Require the first data line to have indentation level zero.
4. If it is exactly `..`, create a root mapping and parse its children at level
   one.
5. If it is exactly `:`, create a root sequence and parse its children at level
   one.
6. If it is exactly `|`, collect a root multiline string using section 10.5.
7. Otherwise, parse the complete line as one raw or quoted root string.
8. After the root has ended, ignore validated blank and comment lines. A
   remaining indented data line is `E_INDENT`; any remaining level-zero data
   line is `E_SYNTAX`.

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

In a mapping, after indentation is removed, classify a line deterministically
in this order:

1. If the line contains no ASCII space and ends with `..`, remove that suffix
   and treat the remainder as the candidate key for a nested mapping.
2. Otherwise, if the line contains no ASCII space and ends with `:`, remove
   that suffix and treat the remainder as the candidate key for a nested
   sequence.
3. Otherwise, if the line contains no ASCII space and ends with `|`, remove
   that suffix and treat the remainder as the candidate key for a multiline
   string.
4. Otherwise, if the line contains no ASCII space, treat the complete line as
   the candidate key for an empty string.
5. Otherwise, split at the first ASCII space. The prefix is the candidate key
   and the complete remainder is a raw or quoted scalar candidate.

After classification, validate the candidate key before validating its value.
Thus `name|` is a multiline header, `name |` is the scalar value `|`, and
`name value |` is the scalar value `value |`. The line `name  |` is a scalar
candidate whose value begins with an ASCII space and is `E_STRING`; `name ` is
a scalar candidate with an empty scalar and is also `E_STRING`.

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

- `E_ENCODING`: invalid UTF-8, a leading UTF-8 signature, a bare CR, or a forbidden
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

This rule selects which error is reported; it does not require a public API to
expose the byte offset. Adapter protocol version 1 transports only the selected
category, so earliest-position behavior is verified by implementation-native
tests and review. A future protocol version may add a position field, but doing
so must follow the protocol compatibility rules in `VERSIONING.md`.

For example, this partial indentation is `E_INDENT`:

```nano-invalid
..
   name Ariana
```

This repeated key is `E_DUPLICATE_KEY`:

```nano-invalid
..
    name Ariana
    name Mark
```

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
..
    name Harvard University
    country USA
    address|
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

The example represents a root mapping. Every scalar—including `20`—is a
string.

## 14. Deferred features

Nano Markup 1.0 does not define canonical serialization, schemas, references,
aliases, includes, templates, executable expressions, or application-specific
type conversion. Such features require a later specification revision.

## 15. Security and resource limits

Nano Markup has no executable directives: comments, keys, and values MUST NOT
change parser configuration or invoke code merely by being parsed.

Implementations MAY limit input bytes, line length, nesting depth, mapping or
sequence size, and decoded string size to protect against resource exhaustion.
Limits and the error reported when they are exceeded MUST be documented. A
decoder MUST apply duplicate-key checks even when processing untrusted input.

## 16. Normative references

- **BCP 14**: [RFC 2119, *Key words for use in RFCs to Indicate Requirement
  Levels*](https://www.rfc-editor.org/info/rfc2119), as updated by
  [RFC 8174, *Ambiguity of Uppercase vs Lowercase in RFC 2119 Key
  Words*](https://www.rfc-editor.org/info/rfc8174).
- **UTF-8**: [RFC 3629, *UTF-8, a transformation format of ISO
  10646*](https://www.rfc-editor.org/info/rfc3629).
- **Unicode terminology**: [The Unicode Standard, Version
  17.0.0](https://www.unicode.org/versions/Unicode17.0.0/). Nano Markup's
  accepted scalar repertoire is defined explicitly in section 2 and is not
  limited to assigned characters in that Unicode version.
