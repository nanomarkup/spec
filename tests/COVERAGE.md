# Nano Markup 0.6-draft conformance coverage

This matrix maps normative behavior to the fixture corpus. A row may group
closely related requirements from one specification section. Expected JSON
contains only data; comments and formatting are intentionally absent.

| Area | Required behavior | Valid coverage | Invalid coverage |
| --- | --- | --- | --- |
| Data model | Strings, mappings, and ordered sequences at any nesting position, including roots; duplicate sequence items remain significant; comparison is code-point exact | `root_raw_string`, `root_mapping`, `root_sequence`, `nested`, `sequence_duplicates`, `unicode_exactness` | `duplicate_key`, `duplicate_nested_key` |
| Encoding | UTF-8 without BOM; representatives from every forbidden C0 range plus DEL and C1; boundary scalar values and noncharacters | Unicode in `root_mapping`, `unicode_exactness` | `utf8_bom`, `invalid_utf8`, `control_character`, `control_u000b`, `control_u000e`, `nul`, `del_control`, `c1_control` |
| Line endings | LF, CRLF, mixed endings, and missing final ending are equivalent | `line_endings_lf`, `line_endings_crlf`, `line_endings_mixed`, `no_final_newline` | `bare_cr` |
| Tabs | Literal tabs are rejected everywhere | Escaped tab in `root_mapping` | `tab_indent`, `tab_scalar` |
| Indentation | Four-space syntax levels; no partial, skipped, or unexpected children; multiple-level dedents; comments validated before removal | `nested`, `multiline_indentation`, `multiple_level_dedent` | `partial_indent`, `skipped_indent`, `unexpected_indent`, `comment_partial_indent`, `comment_only_partial_indent`, `multiline_partial_indent` |
| Keys | ASCII grammar, case-sensitive uniqueness per mapping, reuse across mappings, and near-header rejection | `root_mapping`, `nested`, `key_scopes` | `illegal_key`, `key_starts_digit`, `key_starts_hyphen`, `duplicate_key`, `duplicate_nested_key`, `near_mapping_header`, `near_sequence_header`, `empty_mapping_key_marker`, `empty_sequence_key_marker` |
| Roots | Explicit `..` mapping and `:` sequence; raw, quoted, empty, and `|` multiline strings; empty/blank/comment-only default mapping; reserved root strings quoted; mapping-like text remains a string; exactly one root value | `root_mapping`, `empty_root_mapping`, `root_sequence`, `empty_root_sequence`, `root_raw_string`, `root_quoted_string`, `root_empty_string`, `root_multiline_string`, `root_empty_multiline_string`, `root_mapping_like_string`, `root_named_sequence_like_string`, `root_reserved_mapping_marker`, `root_reserved_sequence_marker`, `root_reserved_multiline_marker`, `root_hash_string`, `empty_document`, `whitespace_only`, `comment_only` | `root_mapping_sibling`, `root_sequence_sibling`, `root_string_sibling`, `root_multiline_sibling`, `root_marker_indented`, `root_string_indented`, `root_quoted_trailing_text`, `root_raw_trailing_space` |
| Containers | Nested and empty mappings/sequences; heterogeneous sequence items; empty containers followed by same-level and differently nested siblings | `nested`, `empty_containers`, `comments_and_empty_containers`, `multiple_level_dedent`, `empty_containers_and_siblings` | indentation fixtures above |
| Raw strings | Ordinary root and nested text; internal spaces, quotes, and `#`; near-marker text; permitted Unicode whitespace is data rather than a blank line | `root_raw_string`, `root_mapping`, `root_unicode_whitespace`, `unicode_whitespace_nested`, `near_markers_sequence`, `raw_internal_spaces`, `mapping_scalar_markers`; writer reserved-root and mapping-string cases | `raw_leading_space`, `raw_trailing_space`, `root_raw_trailing_space`, `empty_after_separator`, `double_space_separator`, `double_space_block_header` |
| Quoted strings | Root and nested empty/reserved strings; every supported escape; quote occupies complete scalar position | `root_quoted_string`, `root_empty_string`, `root_hash_string`, `root_mapping`, `root_sequence` | `bad_escape`, `root_bad_escape`, `unterminated_quote`, `quoted_trailing_text`, `root_quoted_trailing_text` |
| Multiline strings | Root and nested empty blocks, leading/internal/trailing blanks, extra indentation, reserved text, Unicode whitespace content, space-only logical lines, LF normalization | `root_multiline_string`, `root_empty_multiline_string`, `multiline_comments`, `multiline_indentation`, `multiline_edges`, `multiline_line_endings`, `unicode_whitespace_nested`; writer `root_space_only_lines`, `nested_space_only_lines` | `multiline_partial_indent`, `root_multiline_sibling` |
| Comments | Ignored outside blocks; data inside blocks; do not create children or items; complete indentation need not match an open container | `comment_only`, `comments_and_empty_containers`, `multiline_comments`, `comments_arbitrary_indent` | `comment_partial_indent` |
| Errors | Stable error categories and deterministic precedence across every adjacent priority pair | All valid fixtures | All invalid fixtures, especially `error_precedence_encoding`, `error_precedence_tab`, and `precedence_*` |

Writer round trips are exercised by the writer protocol and cross-decoding.
Cyclic containers, unsupported host-language values, documented resource
limits, source-preserving APIs, and the security prohibition on executable
directives require implementation-level tests or review.

See [REQUIREMENTS.md](REQUIREMENTS.md) for the individual normative-keyword
traceability index.
