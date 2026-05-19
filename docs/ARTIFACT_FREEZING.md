# Artifact Freezing

## Purpose
Freeze candidate artifacts (config snapshots, reports, governance reviews) with deterministic hashes for immutability.

## Mechanism
- Calculates payload hash.
- Scans for secrets and broker fields.
- Checks `status` (BLOCKED/INVALID on leak).
- Generates `FrozenArtifact` record.

## Disclaimer
Freezing is local metadata immutability; it does not provide OS-level immutability guarantees.

## CLI Commands
```bash
python -m usa_signal_bot collect-artifacts --write
python -m usa_signal_bot freeze-artifacts --write
python -m usa_signal_bot verify-checksum
```
