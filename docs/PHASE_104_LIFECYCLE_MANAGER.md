# Phase 104 - Runtime Lifecycle Manager

## Overview
Phase 104 builds the metadata-only runtime lifecycle manager. It introduces state machine controls and service readiness evaluations designed exclusively to track local metadata and explicitly denies real broker executions, network fetches, paper mutations, and active paper operations.

## Key Subsystems
* `RuntimeLifecycleStateMachine`: Moves components safely between states (`DRAFT` to `DRY_RUN_VALIDATED`) blocking unsanctioned state changes.
* `LifecycleDryRunValidator`: Provides the strongest defense mechanism, assuring that the dry-run produced `execution_performed=False`, `broker_used=False`, etc.
* `ServiceGraphIngestion`: Extracts read-only components constructed from the Phase 103 review stage and ensures they harbor zero side-effects.

## CLI Usage
Run `python -m usa_signal_bot lifecycle-info` to receive details about the phase, explicitly noting it is NOT an activation run.
Run `python -m usa_signal_bot lifecycle-review` to generate the complete `RuntimeLifecycleFullReview` payload.

## Limitations
This is an evaluation and metadata system only. Generating a "Ready for Phase 105" checkmark equates to passing local evaluations and absolutely DOES NOT approve live trading, investment recommendations, real Telegram notifications, scraping events, or dashboard spin-ups.
