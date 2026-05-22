# Paper-Mode Dry Admission Rehearsal

## Overview
The Paper-Mode Dry Admission Rehearsal is a strictly local metadata layer. It evaluates whether a given strategy candidate is eligible for simulated admission to the active paper trading state, without actually performing the admission.

It is designed to verify the "no-write" and safety conditions required before a candidate can be considered for real paper trading deployment.

## Limitations
- **This dry admission rehearsal is local metadata only.**
- **It does NOT constitute active paper or live trading approval.**
- **No broker API calls, demo or live orders are generated.**
- **No real paper state mutation occurs.**
- **No Telegram real sends occur.**
- **No production configuration patches are applied.**

## Components
1. **Eligibility Checker**: Verifies if the candidate has passed the paper-mode preflight.
2. **Plan Builder**: Constructs the steps for the dry admission rehearsal.
3. **Runner**: Executes the dry admission simulation, ensuring no writes actually occur.
4. **Output Analyzer**: Generates a summary and metadata metrics based on the execution result.

## CLI Usage
To view the status or perform tasks from the command line:

```bash
python -m usa_signal_bot dry-admission-info
python -m usa_signal_bot dry-admission-plan --write
python -m usa_signal_bot dry-admission-run --write
```
