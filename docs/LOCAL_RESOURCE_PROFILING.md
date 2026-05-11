# Local Resource Profiling

This subsystem provides the foundation for Phase 49's local resource profiling capabilities. It generates secure, lightweight snapshots of system resource consumption during specific tasks or logical scopes.

## Core Capabilities
* **Wall-Time and Process-Time**: Uses the Python standard library (`time.perf_counter`, `time.process_time`) to measure task durations accurately without adding dependencies.
* **Memory Allocation Snapshot**: Employs `tracemalloc` to natively assess memory consumption specific to the executing context block (Python objects only).
* **Artifact Footprint**: Inspects localized output trajectories on disk via `pathlib` traversal. Captures size changes dynamically while protecting against directory traversal.

## Key Restrictions
* **No psutil/pynvml**: Total system resource utilization is not measured here, avoiding heavy system-level integration or CUDA bindings.
* **No External Telemetry**: Explicit telemetry fields or datadog/prometheus integrations are aggressively blocked and validated at export.
* **Dry-Run Default**: Local operations default to simple "noop" or estimation traces to avoid side effects.

## CLI Usage

Inspect configured profiling rules:
```bash
python -m usa_signal_bot profiling-info
```

Generate a rapid noop trace:
```bash
python -m usa_signal_bot profile-noop --write
```

Generate a lightweight artifact snapshot trace for a path:
```bash
python -m usa_signal_bot profile-artifacts --path data --write
```
