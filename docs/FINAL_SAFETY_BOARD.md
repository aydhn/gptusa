# Final Safety Board

## Purpose
The Final Safety Board performs a rigorous local metadata gate check on the Promotion Dossier before producing a Staged Readiness Package.

## Gates
- `evidence_complete`: All evidence types are present.
- `evidence_not_stale`: No evidence artifacts have expired.
- `no_active_paper_permission`: `allowed_for_active_paper` must be strictly `False`.
- `no_paper_state_mutation`: `allowed_for_paper_state_mutation` must be strictly `False`.
- `no_order_execution`: `allowed_for_broker_execution` and flags must be `False`.
- `no_config_patch`: `allowed_for_config_patch` must be `False`.

## Limitations
- Safety Board **PASS** is NOT a deployment approval. It solely allows the generation of a non-executing metadata package.

## Commands
- `python -m usa_signal_bot final-safety-board-gates --write`
- `python -m usa_signal_bot final-safety-board-decision --write`
