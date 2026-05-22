# Human Approval Ledger

## Overview
The Human Approval Ledger tracks human review sign-offs for candidate strategies prior to active paper deployment. It mandates explicit acknowledgement that the approval is not an authorization for active trading.

## Limitations
- **Ledger is NOT active paper approval.**
- **Must include `acknowledged_not_activation=True`.**
- **`activation_allowed=False` must be preserved.**
- **Rejects notes containing terms like "aktif et", "canlıya al", "emir gönder", "live approved".**

## CLI Usage
```bash
python -m usa_signal_bot human-ledger-entry --scope not_activation_approval --note "acknowledged no activation" --write
python -m usa_signal_bot human-approval-ledger --write
python -m usa_signal_bot human-approval-validate --write
```
