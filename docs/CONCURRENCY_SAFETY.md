# Concurrency Safety

## Overview
Concurrency policies restrict overlapping executions within defined scopes to maintain safe operations.

## Concurrency Policy
Each `RunLockScope` has a defining `ConcurrencyPolicy` that specifies:
- `max_concurrent_runs`
- `allow_overlap`
- Conflict resolution `acquisition_mode`.

## Conflict Blocking & Deadlocks
If a scope requires serialization (e.g., `SCAN` limit 1), further runs are inherently blocked until the active lock completes or times out. This avoids unintended race conditions. Wait timeouts or `FAIL_FAST` patterns minimize the potential for deadlocks.

## Destructive Commands Guard
Concurrency checks explicitly deny running destructive actions dynamically (e.g., `cleanup-execute` limits overlapping) without explicit human confirmation.

## CLI Example
- `python -m usa_signal_bot concurrency-review --scope scan`
