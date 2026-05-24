# Paper Sandbox Runtime Admission Blocker Replay

## Overview
The Sandbox Runtime Admission Blocker Replay is a core component of Phase 100 in the USA Signal Bot project. Its primary purpose is to retrospectively test and ensure that all prior events, rules, and conditions consistently block sandbox runtime admissions.

## Mechanism
- **Metadata Only:** The replay engine strictly analyzes metadata events representing past admission attempts.
- **Required Attempts:** It looks for specific required attempt types, such as `START_PAPER_SANDBOX_RUNTIME`, `ADMIT_CANDIDATE_TO_SANDBOX_RUNTIME`, `START_SANDBOX_PAPER_SESSION`, etc.
- **Evaluation Criteria:** Every event MUST have `blocked=True` and `sandbox_runtime_admission_allowed=False`. If any event fails this check, the replay fails and the system blocks any further progression.

## CLI Usage
To interact with the replay engine, use the following commands:
- Generate a replay plan:
  `python -m usa_signal_bot sandbox-replay-plan --write`
- Run the replay engine based on the plan:
  `python -m usa_signal_bot sandbox-replay-run --write`
- Analyze the results of the replay:
  `python -m usa_signal_bot sandbox-replay-analyze --write`
