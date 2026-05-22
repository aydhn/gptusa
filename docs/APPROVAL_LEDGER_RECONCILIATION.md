# Approval Ledger Reconciliation

## Purpose
The Approval Ledger Reconciliation subsystem ensures that the human approval ledger from Phase 86 contains all required review scopes and contains no unsafe language.

## Limitations
- **NOT an Activation:** A reconciled ledger does NOT constitute active paper approval or live trading authorization.
- **NO Real Execution:** Reconciling the ledger generates metadata only.

## Required Scopes
- `NO_WRITE_REVIEW_ACKNOWLEDGEMENT`
- `SAFETY_REVIEW_ACKNOWLEDGEMENT`
- `EVIDENCE_REVIEW_ACKNOWLEDGEMENT`
- `NOT_ACTIVATION_APPROVAL`

## Unsafe Note Detection
The system automatically blocks ledgers containing execution or activation terminology such as:
- "aktif et"
- "canlıya al"
- "emir gönder"
- "garanti"
- "kesin al"
- "paper'a uygula"
- "sent to broker"
- "live approved"

## CLI Examples
```bash
python -m usa_signal_bot ledger-reconcile --write
python -m usa_signal_bot admission-no-write-continuity --write
```
