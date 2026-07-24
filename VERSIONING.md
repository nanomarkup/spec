# Nano Markup versioning

Drafts may change incompatibly and use names such as `0.5-draft`. Once a draft
is tagged, later normative changes use a new draft version; tagged text and
fixtures are immutable.

Known mistakes in an immutable release are recorded in `ERRATA.md`. Errata are
informative notices, not silent amendments to a tag. Any correction that
changes normative behavior is published under a new version.

A proposed stable release is tagged `v1.0.0-rc.1`. Release candidates may
receive compatible corrections. A change that invalidates a conforming RC
document or changes its decoded tree requires another RC and restarts the
compatibility period. Each RC compatibility period lasts at least 30 days.
Stable `v1.0.0` is not published while any known correctness, security, or
interoperability release blocker remains unresolved.

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
