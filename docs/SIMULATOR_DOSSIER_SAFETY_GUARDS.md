# Simulator Dossier Safety Guards

- No active paper enable.
- No paper admission.
- No simulator admission.
- No local paper simulator start.
- No sandbox runtime admission.
- No paper sandbox runtime start.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.
- Sandbox runtime admission attempt not blocked -> block.
- Any allowed flag set to true -> block.
- order_created or mutation_detected set to true -> block.

## CLI Examples
`python -m usa_signal_bot simulator-dossier-continuity --write`
`python -m usa_signal_bot simulator-dossier-safety-check --write`
`python -m usa_signal_bot simulator-dossier-validate --latest-review`
