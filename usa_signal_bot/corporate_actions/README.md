# Corporate Action Guard Module

This module provides detection, validation, and guardrails for corporate actions (splits, dividends) in the USA Signal Bot.

## Overview

The corporate action system provides:
- Detection of possible splits and dividends based on price gaps.
- Adjusted close consistency validation.
- Guardrails to block or warn on signals during significant corporate actions.

## Constraints

- Strictly local execution. No paid APIs or scraping.
- Corporate action detections are heuristic and rely on local data or free provider metadata.
- Outputs are for operational use and local guardrails. They are **not investment advice**, **not guarantees**, and **not live trading approvals**.
