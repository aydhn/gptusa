# Backup and Restore (Dry Run)

This outlines how backups are created locally.

## Features
- Backs up configs, reports, cache (optional).
- EXCLUDES all secret-like files.
- Restoring is strictly a "dry-run" process by default, logging conflicts but avoiding real overwrites.

## Operations
```bash
# Create reports backup
python -m usa_signal_bot backup-create --scope reports_only

# Validate a specific backup
python -m usa_signal_bot backup-validate --backup <path_to_backup.zip>

# Dry-run restore
python -m usa_signal_bot restore-dry-run --backup <path_to_backup.zip> --target-dir ./preview
```
