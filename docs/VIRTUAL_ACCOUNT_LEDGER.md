# Virtual Account Ledger

The Virtual Account Ledger provides a local, file-based simulation of an account balance and historical positions.

## Concepts
- **VirtualAccount**: Holds the high-level cash and equity balances, realized and unrealized PnL, and metadata.
- **Starting Cash**: The configured initial balance.
- **CashLedgerEntry**: Every cash impact (buy debit, sell credit, fees) is recorded here chronologically.
- **PaperPosition**: Tracks current asset holdings.
- **PaperEquitySnapshot**: Takes a moment-in-time calculation of overall portfolio value and exposure metrics.

## Scope
This ledger is strictly a **simulation artifact**. It does not reflect, nor link to, any actual bank or broker account.

## Operations
Virtual accounts are managed locally within `data/paper/accounts/`.
All operations are appended safely and do not overwrite prior histories unless manually reset.

## CLI Examples
```bash
# Create a new local paper account with $100k
python -m usa_signal_bot paper-account-create --name local_paper --starting-cash 100000 --write

# View the status
python -m usa_signal_bot paper-account-status --latest
```
