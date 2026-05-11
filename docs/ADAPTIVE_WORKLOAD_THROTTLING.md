# Adaptive Workload Throttling

Adaptive Workload Throttling builds on resource profiling by generating actionable—yet completely passive—hints for task queueing and dispatch adapters.

## Mechanics
Throttling plans match `ResourceProfiles` against preset `ThrottlingPolicy` definitions bound closely to `ResourceProfileScope`s.

If thresholds (like memory allocation ceilings) are breached, the throttling engine sets a severity rank (LOW, MODERATE, HIGH, CRITICAL) and attaches a suggested fallback mechanism.

### Handled Actions
* `ALLOW`: Task execution permitted.
* `WARN`: Triggers metric logging logic.
* `DELAY` / `SPLIT`: Suggests the scheduler push the workload forward or queue executors chunk batches.
* `REDUCE_SCOPE`: Implies tasks like Backtesting should run with a smaller time window.
* `DRY_RUN_ONLY`: Aggressively limits processing.
* `SKIP` / `BLOCK`: Halts specific tasks entirely due to hard limits.
* `REVIEW`: Enforces an operator to acknowledge.

*Note: All actions are stored as METADATA HINTS internally (via taskqueue or scheduler adapters) and do not act as authoritative process-terminators or "Daemons", which are strictly prohibited.*

## CLI Usage
Inspect current active policies or build local plans:
```bash
python -m usa_signal_bot throttling-policies
python -m usa_signal_bot throttling-plan --write
python -m usa_signal_bot throttling-latest
```
