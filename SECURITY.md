# Security policy

## Scope

This repository covers vulnerabilities or specification defects that affect
the Nano Markup language or its conformance tools. Vulnerabilities confined to
one implementation should be reported to that implementation's repository.

Relevant reports include ambiguous parsing that may produce different trees,
ways to bypass forbidden-character or duplicate-key validation, unintended
executable behavior, fixture or adapter integrity problems, and denial-of-
service risks created by normative requirements.

## Reporting

Report sensitive issues privately through the repository's
[GitHub security advisory form](https://github.com/nohainc/nanomarkup.spec/security/advisories/new).
Do not include exploit details in a public issue before coordinated disclosure.
If private reporting is unavailable, open a minimal public issue requesting a
private contact channel without disclosing sensitive details.

Non-sensitive specification ambiguities and conformance gaps may be reported
as ordinary GitHub issues.

## Supported versions

Security analysis focuses on `main` and the newest published specification.
Tagged releases remain immutable. Corrections are published in a new version
and documented in `ERRATA.md` when an older release is affected.
