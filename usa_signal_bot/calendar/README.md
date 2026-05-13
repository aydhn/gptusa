# Calendar and Session Awareness Module

This module provides market calendar, trading session awareness, and session validation capabilities for the USA Signal Bot.

## Overview

The calendar system provides:
- Trading day calculation (weekends, holidays).
- Early close awareness.
- Session classification (REGULAR, PREMARKET, AFTER_HOURS).
- Bar/session alignment validation.

## Constraints

- Strictly local execution. No paid APIs or scraping for market calendars.
- Calendar data relies on local configuration (JSON files) and provider metadata.
- Outputs are for operational use and local guardrails. They are **not investment advice** and **not live trading approvals**.
