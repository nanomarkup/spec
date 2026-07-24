# Releasing the Nano Markup specification

The specification is released independently from every implementation. Python,
Go, or other implementations provide interoperability evidence but are not
part of the normative specification release.

## Release contents

One release is the immutable repository tree identified by an annotated Git
tag. Normative contents are identified in section 1 of `SPEC.md`. GitHub release
archives are conveniences built from that same tag.

## Prerequisites

Before tagging:

1. Confirm that the version agrees in `SPEC.md`, the decoder and writer
   manifests, the byte-integrity manifest, and the examples manifest.
2. Resolve all correctness, security, and interoperability blockers for the
   intended maturity level.
3. Run `python tests/validate.py`, `python tests/validate_links.py`, and
   `python tools/render_spec.py --check` after installing `requirements-docs.txt`.
4. Run `tests/run_conformance.py` with at least two independent adapters and
   retain the successful run URLs or commit identifiers in the release notes.
5. Confirm that every normative requirement is represented in
   `tests/REQUIREMENTS.md` by a fixture, protocol check, native test, or explicit
   review requirement.
6. Replace `Unreleased` in the matching `CHANGELOG.md` heading with the actual
   release date in `YYYY-MM-DD` form.
7. Run `python tests/validate_release.py vVERSION`.
8. Require a green protected `main` branch and a clean working tree.

Configure the GitHub `specification-release` environment with required manual
reviewers before the first tag is pushed. The release workflow uses that
environment and needs permission to create GitHub releases.

## Tag and publish

Create and push an annotated tag only after the release commit is on `main`:

```console
git tag -a v1.0.0-rc.1 -m "Nano Markup 1.0.0-rc.1"
git push origin v1.0.0-rc.1
```

The tag workflow repeats validation, builds `.tar.gz` and `.zip` archives with
a versioned top-level directory, copies the generated HTML specification as a
standalone release asset, creates `SHA256SUMS`, and publishes those files in a
GitHub release. Verify the release page, download the archives and HTML, verify
their checksums, and inspect one extracted archive before announcing it.

Only after the specification release succeeds should implementations update
their pinned specification commit and publish corresponding implementation
versions.

## Promoting a release candidate to stable 1.0

Keep `v1.0.0-rc.1` available for compatibility testing for at least 30 days.
During that period, exercise it through independent implementations and example
applications. Resolve all correctness, security, and interoperability release
blockers. Any semantic change that invalidates an RC document or changes its
tree requires a subsequent RC and restarts the 30-day period.

After a clean compatibility period, change the specification identity and all
manifests to `1.0.0`, add a dated changelog section, repeat every prerequisite
above, and publish the specification tag `v1.0.0`. Matching implementation
`1.0.0` releases follow only after that specification release succeeds.

## Immutability and corrections

Never move, delete, or recreate a public specification tag. Record editorial
mistakes in `ERRATA.md`. A change to normative behavior requires the next
version under `VERSIONING.md`; it is not applied silently to an existing tag.
