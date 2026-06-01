# Baseline Scaffolding Safety Guards

## Forbidden Operations
- No trade signals or order decisions.
- No strategy activations or deployments.
- No portfolio weight generations.
- No investment advice.
- No real broker interaction, paper mutation, or Telegram sends.
- No web scraping, HTML parsing, or paid APIs.
- No daemon, scheduler, or background worker processes.
- No actual ML model training or prediction code execution.
- No hidden API keys or secrets in manifests.

## Language and Column Checks
The text outputs and data frame columns are rigidly scanned to prevent terminology like "buy", "sell", "guaranteed profit", "live order", etc.
