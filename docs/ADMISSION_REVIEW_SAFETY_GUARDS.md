# Admission Review Safety Guards

## Safety Principles
The Admission Review subsystem operates under the strictest safety guards to ensure zero unintended mutations.

- **No Active Paper Enable:** Candidates are never enabled in the active paper environment.
- **No Paper State Mutation:** Internal states like portfolios, cash, or positions are strictly read-only.
- **No Paper Orders:** No simulated paper orders are created or executed.
- **No Broker Orders:** Absolutely no interaction with real or demo broker APIs.
- **No Telegram Real Send:** Notifications are strictly localized dry-runs or generated as preview metadata.
- **No Production Config Patch:** `default.yaml` and other configurations are never modified automatically.

## Blocking Conditions
Any of the following will result in an immediate BLOCK:
- `Ledger activation risk` (i.e. ledger attempts to approve activation)
- `transition_allowed` is True
- `activation_allowed` is True
- Detection of sensitive tokens/secrets

## CLI Examples
```bash
python -m usa_signal_bot admission-safety-check --write
python -m usa_signal_bot admission-review-validate --latest-review
```
