# No-Write Transition Safety Guards

Strict safety guards block transition if any of the following risks are detected:
- No active paper enable.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.
- Any dangerous bridge route blocks transition.
- `activation_allowed` = true blocks transition.
- `transition_allowed` = true blocks transition.

## CLI Commands
- `python -m usa_signal_bot sandbox-bridge-safety-check --write`
- `python -m usa_signal_bot no-write-transition-validate --latest-review`
