# USA Signal Bot - Storage Layer

## Overview
The storage layer provides a standardized interface for interacting with the local file system. It encapsulates file creation, formatting, path resolution, and integrity checks, ensuring that data is persisted safely and predictably across the application.

## Directory Structure
The storage paths are managed under the `data/` root directory. Each sub-directory represents a different type of data (`StorageArea`):

- **raw**: Unprocessed market data.
- **processed**: Transformed/clean data.
- **cache**: Temporary calculations.
- **universe**: Target universe definitions and state.
- **paper**: Paper trading execution records.
- **backtests**: Historical backtest results.
- **reports**: System summaries and performance reports.
- **logs**: Application logs and system audits.
- **features**: Computed feature sets for predictive models.
- **models**: Serialized ML models and scalers.
- **manifests**: Metadata files describing datasets.

## Supported Formats
The storage layer natively supports standard local file formats to keep the project minimal and dependency-free:

- **JSON**: Used for configurations, domain models, and lightweight structured data.
- **JSONL**: Used for append-only data like audit trails and time-series records.
- **CSV**: Used for tabular data exports.
- **PARQUET**: Reserved for future use (when `pandas`/`pyarrow` are introduced). Attempting to use Parquet in the current phase will raise an `UnsupportedOperationError`.

## Safe File Operations
### Path Traversal Protection
All file operations validate paths using `normalize_safe_filename` and `assert_relative_filename`. Furthermore, the `LocalFileStore` and integrity helpers assert that any path resolved mathematically falls strictly under the designated `data/` root directory.

### Atomic Writes
To prevent data corruption during crashes or interruptions, writes default to an atomic approach:
1. Data is written to a uniquely named temporary file.
2. Once complete, the OS's `replace` functionality moves it over the target destination file, providing an atomic swap.

## Usage
The central entry point for file manipulation is the `LocalFileStore` class found in `usa_signal_bot.storage.file_store`:

```python
from usa_signal_bot.storage.file_store import LocalFileStore

store = LocalFileStore(data_dir)
store.ensure_ready()
store.write_json("reports", "summary.json", {"status": "ok"})
```
