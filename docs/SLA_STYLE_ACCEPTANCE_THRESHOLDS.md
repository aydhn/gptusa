# SLA-Style Acceptance Thresholds

SLA-style thresholds define absolute upper bounds on local resource consumption during system operation.

## Notice
These are **NOT formal Service Level Agreements (SLAs)** tied to customer delivery or live broker execution speeds. They act purely as local gating conditions to identify degradation.

## Threshold Levels
1. **Warning**: Operation is slowing or growing slightly beyond safe averages. Consider review.
2. **Critical**: Operation is degrading actively. It will yield `FAIL` status.
3. **Blocker**: Operation is locked in a runaway state. Immediately blocked.

## Core Limits Guarded
- `WALL_TIME_SECONDS`
- `MEMORY_PEAK_MB`
- `OUTPUT_GROWTH_MB`
- `ERROR_COUNT`

## CLI Usage

View Default Set:
```bash
python -m usa_signal_bot sla-thresholds
```

Run Evaluation:
```bash
python -m usa_signal_bot sla-evaluate --write
```

Gate Release Cycle:
```bash
python -m usa_signal_bot performance-acceptance --write
```
