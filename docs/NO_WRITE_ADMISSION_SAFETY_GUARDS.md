# No Write Admission Safety Guards

## Safety Checks
- No active paper enable.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.

## Block conditions
- If `all_writes_blocked` is false -> block.
- If `activation_allowed` is true -> block.
- If there is any preflight write attempt -> block.

## CLI Examples
- `python -m usa_signal_bot runtime-write-lock-assert --write`
- `python -m usa_signal_bot preflight-safety-check --write`
- `python -m usa_signal_bot no-write-admission-validate --latest-review`
