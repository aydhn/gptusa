# Runtime Write-Lock Proof Refresh

## Overview
The Runtime Write-Lock Proof Refresh simulates an attempt to test the write-locking mechanism within the paper-mode. It re-verifies that any attempt to mutate the state of the active paper portfolio, positions, orders, or config will be blocked.

## Limitations
- **Refresh is metadata-only.**
- **It does NOT perform any real write operation.**
- **Requires hash unchanged logic (`hash_unchanged=True`).**
- **Requires `all_writes_blocked=True`.**
- **Requires `mutation_detected=False`.**

## CLI Usage
```bash
python -m usa_signal_bot write-lock-refresh --write
python -m usa_signal_bot write-lock-refresh-validate --write
```
