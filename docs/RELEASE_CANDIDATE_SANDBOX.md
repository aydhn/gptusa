# Release Candidate Sandbox

The Release Candidate Sandbox in the USA Signal Bot provides a localized preview environment to analyze the proposed candidate bundle before it executes in the local or remote production paper configuration setup.

## Purpose
The primary purpose is to preview exactly how a package would modify operation without granting those bundles access to:
* Broker/Live orders
* Paper-trading mutated state
* Live Telegram alerts
* Writing patches or executing auto-tuning updates

## Core Operations
The activation sets a runtime context and mount plan explicitly isolated, building deterministic simulation logic locally inside `data/release_sandbox/outputs`.

## Usage examples
```bash
python -m usa_signal_bot release-sandbox-info
python -m usa_signal_bot sandbox-activation-plan --runtime-mode full_safe_preview --write
python -m usa_signal_bot release-sandbox-review --write
```

Note: PASS flags do NOT symbolize an investment advice or live trade execution.
