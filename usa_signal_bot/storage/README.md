# USA Signal Bot - Storage Layer

This module handles file-based storage operations for the USA Signal Bot project.

It provides a simple, safe, and reliable way to read and write data in standard formats like JSON, JSONL, and CSV. It implements path traversal protection and atomic file writing to ensure data integrity.

## Core Components
- `file_store.py`: Exposes `LocalFileStore` as the primary facade.
- `formats.py`: Defines the supported file formats. Parquet is reserved for future extensions.
- `paths.py`: Manages directory structures under `data/`.
- `manifest.py`: Implements metadata records tracking.
- `integrity.py`: Provides file checksums and size verifications.
