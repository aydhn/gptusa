# Release Candidate Decision Board

## Overview
Decides whether a promotion review translates into a local research release candidate.
Decisions include APPROVE_FOR_MORE_RESEARCH, REJECT, REQUEST_MORE_DATA, REQUEST_RETEST, ACCEPT_AS_LOCAL_RESEARCH_CANDIDATE, and BLOCKED.

## Safety Guardrails
Even when accepted, `allowed_for_auto_apply` and `allowed_for_live_or_demo_execution` remain strictly `False`.

## CLI
```bash
python -m usa_signal_bot decision-board-review --mode conservative --write
python -m usa_signal_bot release-candidate-build --write
```
