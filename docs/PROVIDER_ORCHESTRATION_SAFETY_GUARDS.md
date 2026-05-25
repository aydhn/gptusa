# Provider Orchestration Safety Guards

## Guards Enforced
- **No Trade Signal**: Orchestration data cannot be treated as a signal.
- **No Execution**: No broker orders, paper mutations, or dashboard startups.
- **No Network**: Network usage is blocked for planning components.
- **No Paid APIs / Scraping**: Only local data and fixtures are permitted.
- **Language**: Text validations strip out terms like 'buy', 'sell', 'kesin al', 'emir'.
