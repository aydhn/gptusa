# Phase 145: ML Governance Closure and Explainability

This document describes the Phase 145 explainability metadata, final ML governance closure and Advanced ML band final audit phase.

Phase 145 operates strictly as a read-only ingestion point for Phase 144's `DriftMonitoringFullReview`. It establishes the explainability metadata layer and strictly enforces the final non-activation boundaries for the Advanced ML research band (Phases 136-145).

## Key Components

1. **Drift Monitoring Ingestion**: Safely loads artifacts from the Phase 144 outputs.
2. **Explainability Proxy Layer**: Derives dummy proxy metadata without heavy dependencies (no SHAP/LIME) for model behavior, factors, feature attribution, regimes, and calibration.
3. **Advanced ML Final Audit**: Evaluates the compliance of outputs against the required safety boundaries.
4. **Governance Closure**: Wraps the Advanced ML lineage into a governance summary indicating its readiness.

## Non-Activation Boundary

This phase strictly DOES NOT run:
- Active paper trading
- Deployment or production patches
- Live inference
- Live monitoring
- Live daemons
- Backtests

The explainability artifacts are research diagnostics only, and must not be used as trade signals, portfolio weights, or investment advice.

## Moving to Phase 146
Once the `ready_for_phase146=true` condition is met by passing the `AdvancedMLAcceptanceGate`, the project transitions to Phase 146, the realistic backtest and robustness band.

## CLI Usage

```bash
python -m usa_signal_bot ml-closure-info
python -m usa_signal_bot resolve-explainability-inputs --write
python -m usa_signal_bot build-explainability-report --write
python -m usa_signal_bot build-advanced-ml-final-audit --write
python -m usa_signal_bot ml-closure-review --write
```
