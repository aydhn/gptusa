# Session Awareness

## Overview
Identifies whether a bar aligns with a `REGULAR` trading session, `PREMARKET`, `AFTER_HOURS`, or `CLOSED` times.

## Mechanics
- Examines daily dates and timestamps.
- Intraday uses basic local time comparisons to flag premarket/after-hours.
- Session validation results can adjust `ProviderQualityScore`.

## CLI
`python -m usa_signal_bot calendar-session --date 2024-01-02`
`python -m usa_signal_bot calendar-validate-rows --symbol SPY`
