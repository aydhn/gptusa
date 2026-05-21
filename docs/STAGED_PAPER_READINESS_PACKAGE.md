# Staged Paper Readiness Package

## Purpose
Provides a controlled, four-stage metadata plan outlining how an observer candidate could theoretically transition to paper trading, purely as an exercise.

## Stages
- **Stage 0: Dossier Only:** Initial compilation.
- **Stage 1: Non-Executing Readiness Rehearsal:** Dry-run staging.
- **Stage 2: Guarded Handoff Review:** Metadata safety verification.
- **Stage 3: Final Locked Review:** Final non-executing metadata review.

## Limitations
- Every stage operates with `execution_enabled=False`.
- It is metadata-only and will not unlock or enable real active paper states.

## Commands
- `python -m usa_signal_bot readiness-stage-plan --write`
- `python -m usa_signal_bot staged-readiness-package --write`
