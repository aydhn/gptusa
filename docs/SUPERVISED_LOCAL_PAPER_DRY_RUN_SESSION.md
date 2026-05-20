# Supervised Local Paper Dry-Run Session

## Purpose
The supervised local paper candidate dry-run session runs a quarantined candidate against a read-only snapshot of the active paper runtime. Its primary goal is to safely preview the changes (proposals, risk assessments, and hypothetical notifications) the candidate would make, without touching the live paper state or generating any real actions.

## Lifecycle
1. **Context Building**: The context is assembled from the candidate's promotion ticket, quarantine state, and a read-only paper snapshot.
2. **Proposal Generation**: The system evaluates candidate logic to generate `DryRunProposal` entries.
3. **Risk Evaluation**: Proposals are assessed against mock risk gates to ensure safe scaling, notional bounds, and safety guard adherence.
4. **Notification Preview**: Hypothetical notification messages are formatted to preview alerting behavior.
5. **Human Review Checkpoint**: An explicitly required metadata checkpoint ensures human supervision.
6. **Session Completion**: Results and blocked operations are logged strictly locally.

## CLI Usage
```bash
python -m usa_signal_bot dry-run-bridge-info
python -m usa_signal_bot dry-run-session-run --mode full_supervised_dry_run --write
python -m usa_signal_bot dry-run-bridge-review --write
```
