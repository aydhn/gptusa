# Quarantined Local Paper Candidate

The Quarantined Local Paper Candidate system is a secure governance layer that registers candidates who have successfully passed the shadow-paper rehearsal phase (e.g., `ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE`).

**CRITICAL NOTE**: Enrollment in the quarantine does **NOT** constitute active paper trading enrollment, nor does it approve live or demo broker trading.

## Purpose
It acts as a secure waiting room where candidate bundles are held for manual review, read-only snapshot comparison, and supervised dry-run planning.

## Candidate Statuses
* `DRAFT`: Initial state.
* `ELIGIBLE`: Passed shadow governance thresholds.
* `ENROLLED`: Fully enrolled in quarantine.
* `WAITING_MANUAL_REVIEW`: Waiting for human approval.
* `READY_FOR_SUPERVISED_DRY_RUN`: Ready for dry-run bridge.
* `BLOCKED`: Blocked by safety guards.
* `REJECTED`: Rejected by shadow governance or manual review.
* `EXPIRED`: Review window elapsed.

## CLI Examples
```bash
python -m usa_signal_bot paper-quarantine-info
python -m usa_signal_bot quarantine-eligibility --min-score 70 --write
python -m usa_signal_bot quarantine-enrollment-review --write
```
