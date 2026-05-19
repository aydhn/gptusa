# Safe Local Release Packaging

## Purpose
This subsystem securely packages locally accepted research candidates into versioned, frozen bundles.
It acts as a bridge between research governance (Phase 67) and local deployment.

## Release Candidate Bundle
A bundle is an immutable-ish directory containing the candidate's manifest, artifacts, validations, and a generated README.

## Important Limitations
- **No Production Patching:** It does not modify production config files.
- **No Broker/Live/Demo Execution:** It absolutely does not send live or demo orders.

## CLI Commands
```bash
python -m usa_signal_bot release-packaging-info
python -m usa_signal_bot package-release-candidate --write
python -m usa_signal_bot release-packaging-review --write
```
