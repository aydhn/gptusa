# Atomic IO and Idempotency

## Atomic Writes
To prevent half-written configuration files or locks, all storage is written to a temporary file in the destination folder, then safely moved using `os.replace`.

## Idempotency Key & Duplicate Runs
Before long-running jobs initiate, their exact payload is hashed (ignoring volatile keys like time) into an `idempotency_key`. If the system detects a previous completion corresponding to the same key, it avoids duplicated work based on policies (`SKIP`, `REVIEW`, `BLOCK`).

## Status Tracking
- `IN_PROGRESS`
- `COMPLETED_BEFORE`

## CLI Examples
- `python -m usa_signal_bot atomic-write-test`
- `python -m usa_signal_bot idempotency-summary`
- `python -m usa_signal_bot idempotency-prune --dry-run`
