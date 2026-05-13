# Local Market Calendar

## Overview
Provides an offline local calendar to evaluate trading days, weekends, holidays, and early closes for US equities.

## Constraints
- **Not an Official Calendar**: It relies on heuristics and manual configurations (JSON files). No guarantee of matching actual exchange actions exactly.
- **No Broker API**: Completely local.

## Features
- Validates rows and checks for missing days in daily data.
- Handles manual holidays/early closes.
- Command-line interfaces available:
  `python -m usa_signal_bot calendar-info`
  `python -m usa_signal_bot calendar-write-examples`
  `python -m usa_signal_bot calendar-days --start 2024-01-01 --end 2024-01-31`
