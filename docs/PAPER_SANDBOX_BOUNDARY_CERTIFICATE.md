# Paper Sandbox Boundary Certificate

## Purpose
This acts as the final boundary before any deeper evaluations. It explicitly certificates that the local environment has not mutated paper states, created orders, or made external broker calls.

## Architecture
- Boundary Rules check values like `activation_denied` and `all_writes_blocked`.
- Boundary Assertions verify strictly no-order and no-write boundaries.
- Certificate is metadata-only and does not imply active paper approval.

## CLI Usage
- `python -m usa_signal_bot boundary-rules --write`
- `python -m usa_signal_bot boundary-assertions --write`
- `python -m usa_signal_bot boundary-certificate --write`
