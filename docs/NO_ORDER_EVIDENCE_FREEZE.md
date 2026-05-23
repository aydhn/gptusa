# No-Order Evidence Freeze

## Purpose
The no-order evidence freeze ensures that the no-order dossier and related evaluations are metadata-only, frozen, and immutable before they can be audited.

## Architecture
- Gathers required evidence items (`no_order_dossier_full_review`, `bridge_replay_audit_seal`, etc.).
- Verifies that `frozen=True` and `immutable=True`.
- Generates hashes for verification.

## CLI Usage
- `python -m usa_signal_bot evidence-freeze --write`
- `python -m usa_signal_bot evidence-freeze-validate --write`
