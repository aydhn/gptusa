# Boundary Certificate Safety Guards

The following critical safety checks are enforced:
- No active paper enable (`allows_active_paper=False`).
- No paper admission.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.

If `admission_allowed` is true, or `order_created` is true, the certificate is deemed invalid and blocks the pipeline.

## CLI Usage
- `python -m usa_signal_bot boundary-continuity --write`
- `python -m usa_signal_bot boundary-safety-check --write`
- `python -m usa_signal_bot boundary-validate --latest-review`
