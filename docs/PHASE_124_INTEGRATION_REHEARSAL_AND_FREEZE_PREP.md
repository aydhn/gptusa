# Phase 124 Integration Rehearsal and Freeze Prep

## Purpose
This document outlines the usage of Phase 124 components, providing the end-to-end integration rehearsal, report QA acceptance, and freeze preparation for the Feature/Factor Engine.

## Running the Rehearsal
CLI commands provided in `usa_signal_bot/app/cli.py` can be used:
```bash
python -m usa_signal_bot integration-freeze-info
python -m usa_signal_bot run-integration-rehearsal --write
python -m usa_signal_bot freeze-preparation-review --write
```

These commands will perform the dry run checks, reporting, and acceptance gating, confirming if the artifacts from Phase 116-123 are consistent and completely void of live execution intent or advice language.
