# Nano Markup versioning

Drafts may change incompatibly and use names such as `0.5-draft`. Once a draft
is tagged, later normative changes use a new draft version; tagged text and
fixtures are immutable.

Known mistakes in an immutable release are recorded in `ERRATA.md`. Errata are
informative notices, not silent amendments to a tag. Any correction that
changes normative behavior is published under a new version.

Pre-release development may use release-candidate versions such as
`1.0.0-rc.1`. Release candidates are optional and may receive compatible
corrections. A change that invalidates a conforming RC document or changes its
decoded tree requires another RC if RC testing continues.

A stable release requires a documented review of the normative text and
requirement coverage, successful decoder and writer interoperability evidence
from at least two separate implementations, clean release artifacts, and no
known correctness, security, or interoperability blockers. No minimum elapsed
time is required after that evidence is complete. A project may still choose a
longer observation period when the scope or risk of a future release warrants
one.

Stable `1.x` releases preserve accepted source syntax, decoded data trees,
error categories, and conformance protocol compatibility. Additive
clarifications and fixtures may ship in minor releases. An incompatible
language change requires `2.0.0`.

The stable specification is released before matching implementation releases.
Implementations must expose the exact specification version they support.

The conformance adapter protocol is versioned independently inside
`CONFORMANCE.md`. Additive optional protocol fields may be introduced
compatibly. Removing or reinterpreting a field, changing a required result
shape, or adding a required field creates a new protocol version. A new
protocol must coexist with the preceding stable protocol for at least one
specification release unless a major Nano Markup release explicitly retires it.
