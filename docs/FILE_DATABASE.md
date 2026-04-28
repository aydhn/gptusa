# USA Signal Bot - Local File Database

## Rationale
The USA Signal Bot relies entirely on local file storage rather than external or cloud-hosted database systems. This approach provides:
- Complete data ownership and privacy.
- Zero infrastructure cost or dependency on third parties.
- A simplified development and operational model.
- Easy portability (moving the `data/` folder moves the entire state).

## Data Organization

The file database categorizes data strictly by function into subdirectories inside `data/`:

- **raw market data**: `data/raw/`
- **processed features**: `data/features/` and `data/processed/`
- **universe files**: `data/universe/`
- **paper trades**: `data/paper/`
- **backtests**: `data/backtests/`
- **reports**: `data/reports/`
- **logs/audit**: `data/logs/`
- **manifests**: `data/manifests/`

## Manifest System
To maintain metadata without needing a relational schema, the bot utilizes a Manifest system (`manifests/`). Every major output (such as a backtest result, a feature set, or an ML dataset) generates a manifest record that includes:
- A unique `record_id`.
- Type and format annotations.
- Creation timestamps.
- A cryptographic hash (`checksum_sha256`) for integrity tracking.

## File Integrity and Naming Conventions
Files must be predictably named and verifiable.
- **Integrity**: Files can be validated using their SHA256 checksums mapped in the manifest registry.
- **Naming Constraints**: File names undergo sanitization. Characters that permit directory traversal (such as `..` or `/`) are rejected to secure the file database against malicious or erroneous logic.
