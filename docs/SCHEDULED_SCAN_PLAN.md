# Scheduled Scan Plan

## Overview
Allows configuration of a scan rhythm (interval minutes, max runs).

## Phase Limitations
- OS cron jobs are NOT installed.
- Background daemons are NOT run.
- The `scheduled-scan-next` CLI simply calculates future dates based on settings.
