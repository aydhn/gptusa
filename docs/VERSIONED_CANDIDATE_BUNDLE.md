# Versioned Candidate Bundle

## Purpose
Manage locally generated bundles with semantic-like versioning.

## Details
- Generates semantic-like version based on build number and suffix.
- Relates back to source candidate, experiment, and governance IDs.
- Contains registry for searching bundles.
- Tracks differences via bundle diff.

## CLI Commands
```bash
python -m usa_signal_bot bundle-version --base-version 0.1.0
python -m usa_signal_bot bundle-registry --write
python -m usa_signal_bot bundle-diff --write
```
