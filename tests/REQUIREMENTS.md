# Nano Markup 1.0.0-rc.1 requirement traceability

This index maps each normative `MUST`, `MUST NOT`, and `SHOULD` in `SPEC.md`
to conformance evidence. Algorithm steps inherit the `MUST behave as if`
requirement in section 10 and are mapped by subsection. `MAY` statements grant
options and do not require positive implementation behavior.

Evidence types are:

- **fixture**: a decoder case in `tests/manifest.json`;
- **writer protocol**: a case or invariant enforced by `tests/writer/manifest.json`
  and `tests/run_conformance.py`;
- **native test**: behavior that JSON cannot represent and each implementation
  must test in its own repository;
- **review**: an API, documentation, or security property that cannot be proved
  by a data fixture.

| ID | Normative requirement | Evidence |
| --- | --- | --- |
| CONF-DECODER | A conforming decoder accepts every valid fixture with the expected tree and rejects every invalid fixture with its required category. | Fixture manifest and language-neutral conformance runner. |
| CONF-WRITER | A conforming writer accepts every Nano Markup tree and emits an equivalent decodable tree. | All writer round trips, both newline modes, and cross-decoding by every supplied adapter. |
| CONF-REJECT | A writer rejects values outside the data model without alteration or omission. | Writer invalid cases; native tests for cyclic containers, unsupported host values, invalid keys, forbidden string scalars, and null/nil equivalents. |
| CONF-CLAIM | A conformance claim identifies the exact specification version and every claimed decoder or writer profile. | Release metadata and implementation public-version/API review. |
| MODEL-TREE | A document value is finite and acyclic; repeated noncyclic host containers do not create reference semantics. | Native writer cycle and shared-container tests; writer protocol covers finite JSON trees. |
| MODEL-COMMENT | Adding or removing a comment outside a multiline string does not change the tree. | `comment_only`, `comments_and_empty_containers`, `comments_arbitrary_indent`, `multiline_comments`. |
| MODEL-ROUNDTRIP | `decode(encode(tree))` is equivalent to `tree` for every accepted value. | Writer protocol round trips and cross-reader checks; native randomized round trips. |
| SOURCE-UTF8 | Source is UTF-8 without a leading signature and excludes the specified literal control ranges; interior U+FEFF is data. | `utf8_bom`, `invalid_utf8`, `nul`, `control_character`, `control_u000b`, `control_u000e`, `del_control`, `c1_control`; `interior_bom` and valid boundaries in `unicode_exactness`. |
| SOURCE-WRITER-EOL | One emitted document uses LF consistently or CRLF consistently; LF is preferred unless CRLF is requested. | Writer protocol runs every round trip in both modes and checks physical endings. Default-LF choice is an implementation API review/native test. |
| INDENT-COMPLETE | Every nonblank syntax or comment line starts at a complete four-space level. | `nested`, `multiple_level_dedent`; `partial_indent`, `comment_partial_indent`, `comment_only_partial_indent`. |
| INDENT-SPACE-LINE | A writer quotes strings containing a logical line made only of ASCII spaces. | Writer `root_space_only_lines` and `nested_space_only_lines`; native writer tests. |
| KEY-UNIQUE | Equal keys never occur twice in one mapping. | `duplicate_key`, `duplicate_nested_key`, `key_scopes`. |
| ROOT-EMPTY-STRING | An empty root string is written as `""`. | Writer `root_empty_string`; decoder `root_empty_string`. |
| ROOT-RESERVED | Root values `..`, `:`, `|`, and values beginning with `#` are quoted when serialized as strings. | Writer `root_reserved_string`, `root_reserved_sequence_string`, `root_reserved_multiline_string`, `root_hash_string`; decoder corresponding `root_reserved_*` and `root_hash_string` fixtures. |
| SEQUENCE-EMPTY | An empty sequence string item is written as `""`. | Writer `scalars`; decoder sequence cases in `root_sequence`. |
| SEQUENCE-RESERVED | Sequence string items equal to `..`, `:`, or `|` are quoted. | Writer `scalars`; decoder `near_markers_sequence` and reserved items in `root_sequence`. |
| RAW-BOUNDS | Raw strings are nonempty and do not begin/end with ASCII space, begin with a quote, contain literal TAB/CR/LF, or contain excluded scalars. | Valid raw-string fixtures; `raw_leading_space`, `raw_trailing_space`, `root_raw_trailing_space`, `tab_scalar`, encoding fixtures, quoted-string boundary fixtures. |
| RAW-ROOT-MARKERS | Structural root spellings are quoted when intended as strings. | Same evidence as `ROOT-RESERVED`. |
| QUOTED-COMPLETE | A quoted string occupies the complete scalar position. | `quoted_trailing_text`, `root_quoted_trailing_text`; valid quoted fixtures. |
| COMMENT-IGNORE | A decoder ignores a complete comment line outside multiline content. | `comment_only`, `comments_and_empty_containers`, `comments_arbitrary_indent`. |
| COMMENT-INDENT | Comment indentation uses complete four-space levels. | `comments_arbitrary_indent`; `comment_partial_indent`, `comment_only_partial_indent`. |
| COMMENT-WRITER | A data-tree writer should emit no comments. | Native writer test and implementation review; protocol version 1 does not classify comment-looking output. |
| COMMENT-REMOVAL | Removing comments from a valid document preserves its tree. | Comment fixtures paired with their expected trees; implementation review for source-preserving APIs. |
| PARSE-PREPARE | Section 10.1 preparation order and line handling are observed. | Encoding, tab, LF/CRLF/mixed-ending, bare-CR, no-final-newline, and first two precedence fixtures. |
| PARSE-ROOT | Section 10.2 root classification and single-root rules are observed. | All root fixtures, empty/comment-only documents, root sibling and root indentation invalid fixtures. |
| PARSE-CONTAINER | Section 10.3 indentation, child, dedent, empty-container, and duplicate-key rules are observed. | `nested`, `multiple_level_dedent`, `empty_containers_and_siblings`, `comments_and_empty_containers`; indentation and duplicate invalid fixtures. |
| PARSE-SYNTAX | Section 10.4 recognition order, candidate-key validation, attached mapping markers, and exact forms are observed. | Mapping/sequence fixtures, `mapping_scalar_markers`, `mapping_suffix_values`, `near_markers_sequence`, all separator/near-header/empty-marker invalid fixtures, `malformed_multiline_header`, and `legacy_multiline_header_child`. |
| PARSE-MULTILINE | Section 10.5 collection, blank-line, indentation, and LF-joining rules are observed. | All multiline fixtures, including edge, indentation, line-ending, comment-looking content, Unicode-whitespace, and space-only writer cases. |
| PARSE-TREE | Section 10.6 preserves raw/multiline data, decodes only quoted escapes, and omits presentation metadata. | Raw, quoted, multiline, comment, and `unicode_exactness` fixtures. |
| ERROR-PRIORITY | Multiple errors report `ENCODING > TAB > INDENT > SYNTAX > KEY > DUPLICATE_KEY > ESCAPE > STRING`. | `precedence_encoding_over_tab`, `error_precedence_tab`, and all `precedence_*` fixtures cover every adjacent pair. |
| ERROR-EARLIEST | Within one category, the earliest offending source byte is reported. | Native diagnostic tests and adapter review; protocol version 1 intentionally transports no position. |
| SECURITY-NO-EXEC | Parsing comments, keys, and values never changes parser configuration or invokes code. | Implementation security review; no executable extension points are defined by the syntax or public data APIs. |
| LIMITS-DOCUMENTED | Any resource limits and their errors are documented; duplicate-key checks also apply to untrusted input. | Implementation README/API review plus duplicate-key fixtures and native deep-nesting/fuzz tests. |

The JSON writer protocol deliberately cannot express cyclic object graphs or
implementation-specific value types. Conforming implementations therefore
retain the native checks named by `CONF-REJECT`; passing only the shared JSON
suite is insufficient for writer conformance.
