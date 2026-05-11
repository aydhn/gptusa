# Run Locks

## Overview
This document outlines the file-based run lock system implemented to safely serialize tasks and prevent overlaps in conflicting scopes.

## File-based locks & Scope
Locks are requested by their respective `RunLockScope` (e.g., SCAN, BACKTEST). Each lock captures owner identity (run id, hostname, PID) and stores this state atomically using temporary files and OS replacement.

## Acquire, Heartbeat, Release
- **Acquire**: Acquires the lock utilizing conflict policies (`FAIL_FAST`, `WAIT`, `DRY_RUN`, `STEAL_IF_STALE`).
- **Heartbeat**: Signals the lock is actively being worked on.
- **Release**: Unlocks safely, avoiding unlocking another process's lock.

## Stale Locks
Locks exceeding their configured lifetime without a heartbeat become "stale". Stale locks can optionally be stolen to auto-recover from system crashes.

## Lock Audit
All events are tracked via `lock-audit.jsonl` allowing operators to investigate lock bottlenecks or excessive stale cleanups.

## CLI Examples
- `python -m usa_signal_bot lock-status`
- `python -m usa_signal_bot lock-acquire --scope scan --mode dry_run`
- `python -m usa_signal_bot stale-locks`
- `python -m usa_signal_bot stale-lock-cleanup --dry-run`
