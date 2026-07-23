# Nano Markup 0.4-draft conformance coverage

This matrix maps normative behavior to the fixture corpus. A row may group
closely related requirements from one specification section. Expected JSON
contains only data; comments and formatting are intentionally absent.

| Area | Required behavior | Valid coverage | Invalid coverage |
| --- | --- | --- | --- |
| Data model | Mappings, ordered sequences, strings, duplicates in sequences; mapping or sequence document roots only | `root_mapping`, `root_sequence`, `nested`, `sequence_duplicates` | `duplicate_key`, `duplicate_nested_key`, `root_scalar` |
| Encoding | UTF-8 without BOM; exact C0, DEL, and C1 exclusions | Unicode in `root_mapping` | `utf8_bom`, `invalid_utf8`, `control_character`, `nul`, `del_control`, `c1_control` |
| Line endings | LF, CRLF, mixed endings, and missing final ending are equivalent | `line_endings_lf`, `line_endings_crlf`, `line_endings_mixed`, `no_final_newline` | `bare_cr` |
| Tabs | Literal tabs are rejected everywhere | Escaped tab in `root_mapping` | `tab_indent`, `tab_scalar` |
| Indentation | Four-space syntax levels; no partial, skipped, or unexpected children; comments validated before removal | `nested`, `multiline_indentation` | `partial_indent`, `skipped_indent`, `unexpected_indent`, `comment_partial_indent`, `comment_only_partial_indent`, `multiline_partial_indent` |
| Keys | ASCII grammar, case-sensitive uniqueness per mapping, reuse across mappings | `root_mapping`, `nested`, `key_scopes` | `illegal_key`, `key_starts_digit`, `key_starts_hyphen`, `duplicate_key`, `duplicate_nested_key` |
| Roots | Implicit mapping, explicit `:` sequence, zero-byte/blank/comment-only mapping, empty sequence | `root_mapping`, `root_sequence`, `empty_document`, `whitespace_only`, `comment_only`, `empty_root_sequence` | `root_scalar`, `root_sequence_sibling` |
| Containers | Nested and empty mappings/sequences; heterogeneous sequence items | `nested`, `empty_containers`, `comments_and_empty_containers` | indentation fixtures above |
| Raw strings | Ordinary text and `#` within mapping values | `root_mapping` | `raw_leading_space`, `raw_trailing_space`, `empty_after_separator` |
| Quoted strings | Empty and reserved strings; every supported escape; quote occupies complete scalar position | `root_mapping`, `root_sequence` | `bad_escape`, `unterminated_quote`, `quoted_trailing_text` |
| Multiline strings | Empty blocks, leading/internal/trailing blanks, extra indentation, reserved text, LF normalization | `multiline_comments`, `multiline_indentation`, `multiline_edges`, `multiline_line_endings` | `multiline_partial_indent` |
| Comments | Ignored outside blocks; data inside blocks; do not create children or items | `comment_only`, `comments_and_empty_containers`, `multiline_comments` | `comment_partial_indent` |
| Errors | Stable error categories and deterministic precedence | All valid fixtures | All invalid fixtures, especially `error_precedence_encoding` and `error_precedence_tab` |

Writer requirements, documented resource limits, source-preserving APIs, and
the security prohibition on executable directives require implementation-level
review or round-trip tests and are not fully exercised by decoder protocol
version 1.
