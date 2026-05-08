# Release Candidate Rehearsal

## Overview
The Release Candidate Rehearsal orchestrates the end-to-end regression and evaluates the pipeline's suitability for a "local release".

## ReleaseCandidateStatus
- `PASSED`: All required steps succeeded without critical drift.
- `PASSED_WITH_WARNINGS`: Some non-critical warnings or non-failing drifts were detected.
- `FAILED`: A required step failed, or `fail_on_snapshot_drift` triggered a failure.
- `BLOCKED`: Serious execution violations (e.g., live orders detected).
- `INSUFFICIENT_DATA`: Missing fixtures or baseline data.

## Critical Limitation
**A "PASS" result from the Release Candidate Rehearsal does NOT constitute an approval for live trading or investment advice.**

## CLI Example

```bash
python -m usa_signal_bot release-rehearsal --scope golden_sample --write
```
