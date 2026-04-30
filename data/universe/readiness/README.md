# Universe Readiness Gate

This directory contains the latest Universe Readiness Gate outputs.

- `eligible_symbols.csv`: Symbols that passed the quality and coverage gates.
- `ineligible_symbols.csv`: Symbols that failed the gates (due to missing data, lack of primary timeframe, etc).
- `eligible_symbols.txt`: A plain text list of eligible symbols.

In future phases, the Feature Engine will read directly from the `eligible_symbols` list to ensure only high-quality data is processed.
