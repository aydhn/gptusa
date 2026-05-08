# Operator Runbook

This guide covers operational usage of the USA Signal Bot in a local setup.

## Daily Operation
1. `python -m usa_signal_bot validate-config`
2. `python -m usa_signal_bot health`
3. `python -m usa_signal_bot maintenance-check --frequency daily`
4. `python -m usa_signal_bot scan-dry-run`

## Regression and Quality
- Regression Smoke: `python -m usa_signal_bot regression-info`
- Quality Gate Evaluation: `python -m usa_signal_bot acceptance-evaluate`

## Paper Dry-Run & Notification
Ensure that settings restrict actual broker usage and external communications. By default, paper trading behaves as a dry-run log without executing trades externally.
- `python -m usa_signal_bot notification-dispatch-dry-run`

## Generating the Runbook locally
Run: `python -m usa_signal_bot runbook-generate --write`
