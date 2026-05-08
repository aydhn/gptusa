# Local Release Packaging

The Local Release Packaging system packages the USA Signal Bot for local use.

It does not generate an executable, nor does it connect to any live broker or production systems. It creates a ZIP archive (`data/release/builds/...`) containing source code, configs, test suites, reports, and runbooks.

## Release Components

1. **Manifest**: Records versions and checksums of included artifacts.
2. **Operator Runbook**: Detailed operational guide.
3. **Changelog**: Generated automatically from phase summaries.
4. **Safety Limitations**: Emphasized across all artifacts; ensures users know the tool is exclusively for local research.

## Safety Measures

- **No Secrets**: Configuration actively ignores/blocks any files that appear to contain secrets (`.env`, `token`, `credentials`).
- **No Broker/Live/Demo Integration**: The packaging avoids including any logic that could generate live trades.
- **Not a Live Approval**: A successful release bundle build is not an endorsement to trade the strategy.

## Common CLI Commands

```bash
# View release settings and safety limits
python -m usa_signal_bot release-info

# Build a local release zip
python -m usa_signal_bot release-build-local --write

# Validate latest release bundle
python -m usa_signal_bot release-validate --latest
```
