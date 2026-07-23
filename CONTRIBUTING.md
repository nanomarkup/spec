# Contributing to the Nano Markup specification

Nano Markup is currently an unstable draft. Clear problem statements and small,
testable changes are preferred over adding features preemptively.

## Proposing a change

A proposal should include:

1. The problem in the current specification.
2. The proposed syntax and resulting data model behavior.
3. At least one valid example and its expected data tree.
4. Invalid or ambiguous examples affected by the change.
5. Compatibility and migration consequences.

Normative changes must update `SPEC.md`, `grammar.ebnf` when applicable, the
conformance fixtures, and `CHANGELOG.md` together.

Comments and formatting proposals must distinguish changes to the data model
from changes to the presentation or document model. A presentation feature
must not silently add fields or values to the decoded data tree.

## Design principles

- Prefer one unambiguous spelling for each structure.
- Keep the core data model small and language-neutral.
- Do not add implicit typing or executable behavior to the core language.
- Make malformed input fail rather than silently reinterpret it.
- Keep implementations independent from the specification repository.

## Pull requests

Keep each pull request focused on one language decision. A pull request should
not describe a behavior as normative until matching fixtures exist. Changes to
stable versions, once published, must remain backward compatible unless they
start a new major version.

Contributions are accepted under the repository's CC BY 4.0 license.
