# Human-Approved Non-Executing Paper Observer

The Human-Approved Non-Executing Paper Observer is a governance construct in Phase 76.

## Purpose
The primary purpose of this subsystem is to securely bridge a candidate strategy from a controlled planning approval stage into a read-only "observer" state running parallel to the active paper trading runtime.

## Non-Executing Nature
Human approval of a controlled planning ticket **DOES NOT** constitute an active paper deployment.

The observer subsystem strictly enforces this non-executing boundary:
*   **No Active Paper Enable:** Observer enrollment does not toggle the strategy to "active".
*   **No Real Paper Mutation:** Observer execution does not mutate the active `paper_store` state, the `paper_state_committed` flag, or the portfolio balance.
*   **No Broker Execution:** Observer execution explicitly prohibits routing orders to a live or demo broker.
*   **No Configuration Patches:** Observer enrollment does not write to production configurations.
*   **No Real Telegram Sends:** The observer generates notification *previews* only.

## Enrollment Statuses
The lifecycle of an observer enrollment includes the following statuses (`PaperObserverEnrollmentStatus`):
*   `DRAFT`: Missing full approval.
*   `ELIGIBLE`: Candidate holds an `APPROVED_FOR_NEXT_NON_EXECUTING_STAGE` planning status.
*   `ENROLLED`: Active within the observer subsystem.
*   `LOCKED`: Enrolled with a fully constrained, locked observer policy.
*   `MONITORING`: Actively tracking the read-only paper snapshot.
*   `COMPLETED`: Evaluation finished.
*   `BLOCKED`: Invalid properties detected.
*   `REJECTED` / `EXPIRED` / `ARCHIVED`.

## CLI Usage
Get configuration information and safety limitations:
```bash
python -m usa_signal_bot paper-observer-info
```

Generate an observer enrollment payload:
```bash
python -m usa_signal_bot observer-enrollment --write
```
