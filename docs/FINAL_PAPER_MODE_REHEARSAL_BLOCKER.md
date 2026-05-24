# Final Paper Mode Rehearsal Blocker

## Purpose
The Rehearsal Blocker acts as the ultimate simulation boundary, taking incoming rehearsal attempts (such as starting a paper rehearsal, creating orders, committing paper state) and strictly blocking them while returning an immutable, detailed block event.

## Crucial Note
**The Blocker does NOT open active paper or rehearsal modes. It acts solely to simulate and block rehearsal attempts as metadata.**

## Rule Coverage
It handles the following attempt types, all defaulting to a blocking action (`DENY` or `DENY_AND_RECORD`):
- START_PAPER_MODE_REHEARSAL
- START_LOCAL_PAPER_REHEARSAL_RUNTIME
- REHEARSE_CANDIDATE
- ADMIT_CANDIDATE_TO_REHEARSAL
- CREATE_REHEARSAL_SESSION
- CREATE_PAPER_SESSION
- CREATE_PAPER_ORDER
- COMMIT_PAPER_STATE
- PATCH_PAPER_CONFIG
- SEND_BROKER_ORDER
- SEND_TELEGRAM_REAL
- UNLOCK_REHEARSAL_GATE

## CLI Examples
```bash
python -m usa_signal_bot rehearsal-blocker-rules --write
python -m usa_signal_bot rehearsal-blocker-evaluate --attempt-type start_paper_mode_rehearsal --write
python -m usa_signal_bot rehearsal-attempt-simulate --write
```
