# Alert Policy Layer

The Alert Policy Layer is a local evaluation engine designed to intercept and evaluate various stages of the USA Signal Bot (scans, candidate generation, risk checks, portfolio construction) before generating any notification.

## Key Concepts

- **AlertPolicy**: A rule definition associated with a `scope`, an `alert_type`, and a `severity`.
- **AlertCondition**: Logic criteria assigned to an `AlertPolicy`. Supports comparison operators (GT, LT, IN, BETWEEN, EXISTS, etc.).
- **AlertEvaluationContext**: Extracted payload details provided by the orchestrator step to be evaluated.
- **AlertDecision**: The final outcome of policy evaluation (e.g., ROUTED, SUPPRESSED).
- **AlertEvaluationResult**: The combined evaluation of all policies in a single pass.

## Core Behaviors
- Checks are deterministic and rule-based.
- Built-in duplicate and cooldown suppression (`AlertCooldownManager`) prevent notification spam.
- Threshold values are user-configured defaults.

## CLI Tools
You can manage and test alert policies natively through the CLI without side-effects:

```bash
python -m usa_signal_bot alert-info
python -m usa_signal_bot alert-policy-list
python -m usa_signal_bot alert-policy-preview --scope scan
```

> **Warning:** This layer is strictly for notification routing and does NOT generate real, paper, or dummy broker trades.
