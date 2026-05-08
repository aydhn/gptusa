# Configuration Profiles

Profiles alter the bot's runtime behavior by injecting different base settings.
Broker and actual communication flags are hardcoded to False to maintain safety during local research.

## Available Default Profiles
- `research.yaml`: Basic local research without paper trading and dry-run notifications.
- `paper_dry_run.yaml`: Enables simulated paper executions (dry run only).
- `regression_only.yaml`: Enforces no external network fetches.
- `notification_dry_run.yaml`: Logs notifications instead of dispatching them over the internet.

## CLI Usage
```bash
# List default profiles
python -m usa_signal_bot config-profile-list

# Write defaults
python -m usa_signal_bot config-profile-write-defaults

# Validate profiles
python -m usa_signal_bot config-profile-validate --all
```
