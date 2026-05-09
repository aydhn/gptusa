# Local Incident Response

## Overview
This document describes the USA Signal Bot's local incident response system.
The system is explicitly designed for local, offline operational review.

There are no external integrations (PagerDuty, Datadog, Slack webhooks), and it does not make financial decisions or route live broker orders. It exists to classify failures across the bot's runtime (data, scanning, features, backtests) and produce locally stored summary reports to assist the human operator.

## Incident Sources
Incidents can originate from:
- `RUNTIME`: Background execution failures
- `SCAN`: Candidate scanning anomalies
- `DATA`: Data fetching/consistency issues
- `QUALITY`: Strategy acceptance gate failures
- `REGRESSION`: End-to-end regression test failures
- `RELEASE`: Packaging/manifest errors
- `RETENTION`: Disk quota or protected path cleanup violations
- `OBSERVABILITY`: Health check or log rotation errors

## Categories and Severities
Categories include `CONFIG_ERROR`, `DISK_QUOTA`, `SAFETY_VIOLATION`, `SECRET_LEAK_RISK`, `REGRESSION_FAILURE`, etc.
Severity levels range from `INFO` to `BLOCKER`. A `SECRET_LEAK_RISK` or `SAFETY_VIOLATION` is immediately escalated to `BLOCKER`, halting automated recovery.

## CLI Commands
Review incidents from the latest artifacts:
```bash
python -m usa_signal_bot incident-info
python -m usa_signal_bot incident-review --write
python -m usa_signal_bot incident-latest
```
