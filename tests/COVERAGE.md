# Nano Markup 0.3-draft conformance coverage

This matrix maps normative behavior to the fixture corpus. A row may group
closely related requirements from one specification section. Expected JSON
contains only data; comments and formatting are intentionally absent.

| Area | Required behavior | Valid coverage | Invalid coverage |
| --- | --- | --- | --- |
| Data model | Mappings, ordered sequences, strings, duplicates in sequences | `root_mapping`, `root_sequence`, `nested` | `duplicate_key`, `duplicate_nested_key` |
| Encoding | UTF-8 without BOM; forbidden bytes rejected | Unicode in `root_mapping` | `utf8_bom`, `invalid_utf8`, `control_character` |
| Line endings | LF, CRLF, mixed endings, and missing final ending are equivalent | `line_endings_lf`, `line_endings_crlf`, `line_endings_mixed`, `no_final_newline` | `bare_cr` |
| Tabs | Literal tabs are rejected | Escaped tab in `root_mapping` | `tab_indent` |
| Indentation | Four-space syntax levels; no partial, skipped, or unexpected children | `nested`, `multiline_indentation` | `partial_indent`, `skipped_indent`, `unexpected_indent`, `comment_partial_indent`, `multiline_partial_indent` |
| Keys | ASCII grammar, case-sensitive uniqueness per mapping | `root_mapping`, `nested` | `illegal_key`, `duplicate_key`, `duplicate_nested_key` |
| Roots | Implicit mapping, explicit `:` sequence, empty/comment-only mapping | `root_mapping`, `root_sequence`, `comment_only` | `root_scalar`, `root_sequence_sibling` |
| Containers | Nested and empty mappings/sequences; heterogeneous sequence items | `nested`, `empty_containers`, `comments_and_empty_containers` | indentation fixtures above |
| Raw strings | Ordinary text and `#` within mapping values | `root_mapping` | `raw_leading_space`, `raw_trailing_space` |
| Quoted strings | Empty and reserved strings; every supported escape | `root_mapping`, `root_sequence` | `bad_escape`, `unterminated_quote` |
| Multiline strings | Empty blocks, leading/internal/trailing blanks, extra indentation, reserved text, LF normalization | `multiline_comments`, `multiline_indentation`, `multiline_edges`, `multiline_line_endings` | `multiline_partial_indent` |
| Comments | Ignored outside blocks; data inside blocks; do not create children or items | `comment_only`, `comments_and_empty_containers`, `multiline_comments` | `comment_partial_indent` |
| Errors | Stable error-category reporting for isolated failures | All valid fixtures | All invalid fixtures |

Writer requirements, documented resource limits, source-preserving APIs, and
the security prohibition on executable directives require implementation-level
review or round-trip tests and are not fully exercised by decoder protocol
version 1.
