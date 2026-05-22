# Zero Mutation Audit

Validates that a process has not mutated the underlying paper state by verifying before/after baseline hashes and mutation invariants.

## Key Principles
- **Baseline Hashing:** Takes a read-only snapshot.
- **Invariants:** NO_STATE_COMMITTED, NO_ORDER_EXECUTED, etc.
- **Not an activation:** Passing the audit is not an approval for live trading.

## Commands
```bash
python -m usa_signal_bot zero-mutation-baseline --baseline-type before --write
python -m usa_signal_bot zero-mutation-audit --write
python -m usa_signal_bot mutation-invariant-check --write
```
