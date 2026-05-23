# Paper Sandbox Bridge Safety Guards

Strict limitations are in place to ensure:
- No active paper enable.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.
- Dangerous route allowed flags block operations.
- `activation_allowed=true` or `transition_allowed=true` will block.

## CLI Examples
`python -m usa_signal_bot dangerous-route-validate --write`
`python -m usa_signal_bot bridge-no-write-continuity --write`
`python -m usa_signal_bot bridge-safety-check --write`
`python -m usa_signal_bot bridge-validate --latest-review`
