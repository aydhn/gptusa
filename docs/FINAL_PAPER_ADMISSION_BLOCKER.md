# Final Paper Admission Blocker

## Purpose
The Final Paper Admission Blocker is the ultimate safety net. It explicitly blocks and denies any simulated admission attempts.

## Coverage
All operations that would normally mutate paper state or send orders are explicitly blocked:
- ENABLE_ACTIVE_PAPER
- ADMIT_CANDIDATE_TO_PAPER
- CREATE_PAPER_ORDER
- COMMIT_PAPER_STATE
- SEND_BROKER_ORDER
- SEND_TELEGRAM_REAL

## CLI Usage
- `python -m usa_signal_bot admission-blocker-rules --write`
- `python -m usa_signal_bot admission-attempt-simulate --write`
