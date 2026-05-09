# Safe Rollback Workflow

## Overview
The safe rollback workflow allows the operator to restore the system to a previous known-good state using local sources.

## Rollback Sources
Supported local rollback source types:
- `RELEASE_BUNDLE`: Zip files generated during the release process.
- `BACKUP_ARCHIVE`: Zip backups manually created by the operator.
- `CONFIG_PROFILE`: Previous valid `.yaml` configuration files.
- `REGRESSION_BASELINE`: Golden JSON fixtures used for stability testing.

## Safety Controls
- **Precheck Validation:** Before execution, a precheck verifies checksums, ensures paths are safe relative paths, and blocks payloads containing sensitive secrets.
- **Protected Paths:** Source code (`.py`), configuration (`.yaml`), tests, and documentation are strictly protected and will never be overwritten by an automated rollback.
- **Execution Disabled by Default:** `rollback.execute_enabled` defaults to `False` in the configuration. Unless this is explicitly turned on by the user, all rollbacks are dry-runs that modify no files.

## CLI Commands
Discover sources and simulate a rollback:
```bash
python -m usa_signal_bot rollback-sources
python -m usa_signal_bot rollback-precheck --latest-source --write
python -m usa_signal_bot rollback-plan --latest-source --dry-run --write
python -m usa_signal_bot rollback-dry-run --latest-plan --write
```
