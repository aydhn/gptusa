# Bundle Validation & Checksums

## Validation
- Manifest validation (missing required artifacts).
- Checksum verification for payloads.
- Compatibility checking against supported schemas.
- Safety flags (secret risk, live execution language risk).

## Note
Validation PASS is **NOT** a live trading approval. It simply means the local research artifact is structurally valid and safely packaged.

## CLI Commands
```bash
python -m usa_signal_bot build-manifest --write
python -m usa_signal_bot scan-bundle-safety --write
python -m usa_signal_bot validate-bundle --write
```
