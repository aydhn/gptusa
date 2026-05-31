# ML Dataset Source Resolution

Validates references to dataset sources without allowing execution or leaking secrets.

- Verifies paths using path-traversal safety.
- Asserts file existence and row/column counts.
- Rejects files containing "forbidden output fields" (e.g. `buy`, `sell`, `order`).
