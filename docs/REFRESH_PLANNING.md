# Refresh Planning

## Overview
Identifies symbols that are missing, stale, or low quality and builds a refresh priority list.

## Rules
- Generates a dry-run plan.
- `network_allowed_now` is strictly `False`.
- Does **not** trigger real data fetching operations.
