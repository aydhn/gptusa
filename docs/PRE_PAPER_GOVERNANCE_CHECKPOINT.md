# Pre-Paper Governance Checkpoint

The pre-paper governance checkpoint evaluates the sealed readiness archive against a set of safety gates.

**Important Limitations:**
- A decision of `PASS_TO_GUARDED_PRE_PAPER_DRY_REHEARSAL` is NOT an active paper enable. It only permits progression to Phase 81's dry rehearsal.
- It does not authorize paper state mutation.

CLI Usage:
```
python -m usa_signal_bot pre-paper-checkpoint-gates --write
python -m usa_signal_bot pre-paper-checkpoint-decision --write
```
