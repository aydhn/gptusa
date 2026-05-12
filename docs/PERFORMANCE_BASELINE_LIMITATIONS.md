# Performance Baseline Limitations

This subsystem is designed intentionally within strict, bounded parameters to enforce absolute local isolation.

1. **Hardware Dependent Statistics**: `P90` percentiles directly rely on the host machine. You cannot reliably transplant performance profiles between a server-class host and a consumer laptop.
2. **Not Formal SLAs**: Internal performance thresholds act as software quality gates. They make no claims or guarantees toward market execution speed.
3. **Financial Signal Independence**: Passing or accelerating baselines are purely operational improvements. They do **not** reflect alpha viability, trading returns, or "better" models.
4. **No Investment Advice**: A `PASS` rating simply states your hardware is running the pipeline within bounded time metrics. It does not mean the pipeline is profitable.
5. **No Telemetry Constraints**: We explicitly strip hooks for Sentry, Datadog, Prometheus, etc. Operations are text-based or json-file bounded.
6. **No GPU Tracking**: Deep hardware driver inspections using NVML or psutil were specifically avoided to preserve pure-python installation boundaries.

By reading this text, the operator understands this system produces simulated benchmarks solely for maintenance insight.
