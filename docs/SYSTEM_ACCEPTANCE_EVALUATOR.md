# System Acceptance Evaluator

The System Acceptance Evaluator is the topmost abstraction governing system validation, integrating the Research Quality Scorecard and the Production Readiness Gate into a single PASS/WARN/FAIL decision.

## Process Workflow

1. **Artifact Collection:** Gathers indices and run states from previously completed components (data, features, strategies, walk-forward, baskets).
2. **Scorecard Generation:** Builds the Research Quality Scorecard utilizing artifact presence and content evaluations.
3. **Readiness Evaluation:** Feeds the scorecard into the Production Readiness Gate to execute predefined logic rules.
4. **Decision Mapping:** Interprets the Gate's status into an actionable outcome.

## Acceptance Decisions

- `ACCEPTED_FOR_LOCAL_RESEARCH`: System passed the gate successfully with no warnings or blocking issues.
- `ACCEPTED_WITH_WARNINGS`: System passed core constraints, but non-critical issues or warnings exist.
- `NOT_ACCEPTED`: The gate failed on one or multiple mandatory rules. Resolution of "Required Actions" is necessary.
- `BLOCKED`: Encountered explicitly forbidden rules (e.g. `live_order` flag present, missing critical data).
- `INSUFFICIENT_DATA`: Cannot produce a decision due to sparse or non-existent evaluation artifacts.

## CLI Usage

Evaluate and Write Acceptance Report:
```bash
python -m usa_signal_bot acceptance-evaluate --scope full_local_stack --write
```
