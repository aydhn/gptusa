# No-Order Paper Session Dossier

## Purpose
The No-Order Paper Session Dossier packages outputs from the dry-run, no-order session, and bridge replay processes into a single immutable metadata dossier.

## Limitations
- It is NOT an active paper admission or deployment.
- It does NOT execute real broker or demo orders.
- It does NOT mutate real paper state or configurations.
- It relies on metadata collected from previous bridge components.

## CLI Usage
- `python -m usa_signal_bot no-order-evidence --write`
- `python -m usa_signal_bot no-order-dossier --write`
- `python -m usa_signal_bot no-order-review --write`
