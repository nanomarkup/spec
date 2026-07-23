# Nano Markup versioning

Drafts may change incompatibly and use names such as `0.5-draft`. Once a draft
is tagged, later normative changes use a new draft version; tagged text and
fixtures are immutable.

A proposed stable release is tagged `v1.0.0-rc.1`. Release candidates may
receive compatible corrections. A change that invalidates a conforming RC
document or changes its decoded tree requires another RC and restarts the
compatibility period.

Stable `1.x` releases preserve accepted source syntax, decoded data trees,
error categories, and conformance protocol compatibility. Additive
clarifications and fixtures may ship in minor releases. An incompatible
language change requires `2.0.0`.

The stable specification is released before matching implementation releases.
Implementations must expose the exact specification version they support.
