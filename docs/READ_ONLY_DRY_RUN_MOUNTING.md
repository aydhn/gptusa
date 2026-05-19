# Read-Only Dry-Run Mounting

The Mount Planner in USA Signal Bot securely assigns logic blocks to separate bundle execution parameters locally, enforcing copy-on-write limitations over sandbox actions while isolating operations.

## Allowed Operations
* Extracting configs
* Preview Signal / Portfolios
* Dry running output structures locally

## Denied Operations
* Executing live commands
* Committing back network routines
* Producing order instructions

Source Bundles maintain read-only protection avoiding direct overwrites and conflict overlaps natively.

## Usage Examples
```bash
python -m usa_signal_bot sandbox-read-only-verify
python -m usa_signal_bot sandbox-mount-plan --write
python -m usa_signal_bot sandbox-output-path
```
