# Read-Only Promotion Ticket

A `ReadOnlyPromotionTicket` is a governance metadata record generated for a quarantined candidate.

## Purpose
It provides an auditable, read-only tracking mechanism for a candidate's journey from shadow governance to the dry-run bridge.

## Limitations
* **Not a Deployment Ticket**: This ticket does not deploy code or strategies.
* **Read-Only**: `read_only` is always `True`.
* **No Active Paper**: `allowed_for_active_paper` is strictly `False`.
* **No Config Patch**: `allowed_for_config_patch` is strictly `False`.
* **No Broker Execution**: `allowed_for_broker_execution` is strictly `False`.

## Risk Flags and Manual Review
The ticket tracks risk flags (e.g., potential broker field leaks) and explicitly manages the `manual_review_completed` state.

## CLI Example
```bash
python -m usa_signal_bot promotion-ticket-build --write
```
