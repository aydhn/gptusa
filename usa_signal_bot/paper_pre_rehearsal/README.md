# Paper Pre-Rehearsal Module

This module implements the Guarded Pre-Paper Dry Rehearsal, Paper-State Mutation Firewall, and Activation-Denied Checkpoint for the USA Signal Bot.

## Overview

- `pre_rehearsal_models.py`: Core dataclasses (Plan, Run, Firewall rules/events, Checkpoints, Audits).
- `final_handoff_ingestion.py`: Ingests the Phase 80 final handoff and evaluates it.
- `eligibility_checker.py`: Determines if a candidate is eligible for the pre-paper dry rehearsal.
- `dry_rehearsal_plan.py`: Builds the execution plan (always forces safe flags).
- `paper_baseline_loader.py`: Safely loads and redacts a read-only snapshot of the paper baseline.
- `firewall_rules.py` & `mutation_firewall.py`: Defines and executes the mutation firewall.
- `mutation_attempt_detector.py` & `forbidden_operation_simulator.py`: Detects and simulates dangerous operations.
- `dry_rehearsal_runner.py`: The guarded runner that performs the dry rehearsal.
- `rehearsal_output_analyzer.py`: Analyzes the outputs of the runner.
- `activation_denied_checkpoint.py` & `checkpoint_validator.py`: Creates and validates the mandatory activation-denied checkpoint.
- `zero_mutation_assertion.py`: Asserts that the read-only paper baseline was not mutated.
- `pre_rehearsal_audit.py` & `pre_rehearsal_report.py`: Audit and reporting generation.
- `pre_rehearsal_store.py`: Local JSON/JSONL storage handlers.
- `pre_rehearsal_validation.py` & `pre_rehearsal_reporting.py`: Validation and formatting of outputs.
- `*_adapter.py`: Adapters to bridge with final handoff, readiness rehearsal, promotion dossier, and the existing paper runtime.

## Limits
- Completely local and offline.
- No live broker interactions.
- No active paper state mutations.
- No Telegram sends.
