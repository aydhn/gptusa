# Severity Routing

Severity Routing applies conditional delivery mapping based on the evaluated severity of an `AlertDecision`.

## Priorities & Severity
`AlertSeverity` encompasses five main tiers:
1. `INFO`
2. `NOTICE`
3. `WARNING`
4. `HIGH`
5. `CRITICAL`

## Minimum Severity Guards
A `min_severity_to_route` acts as a base threshold. Alerts below this limit are suppressed with a `SEVERITY_FILTERED` reason.

## Target Routing
The `AlertRouteTarget` denotes where a message intends to go (`DRY_RUN`, `LOG_ONLY`, `FILE`, `TELEGRAM`).
However, for structural safety, the actual dispatcher limits dispatch strictly using the global application configuration.

Example checking dispatch in dry-run mode:
```bash
python -m usa_signal_bot alert-dispatch-dry-run --latest-scan --write
```
