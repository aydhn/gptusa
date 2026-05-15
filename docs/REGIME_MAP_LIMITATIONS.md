# Regime Map Limitations

- **Heuristic Nature**: The regime classifications are based on hardcoded, heuristic thresholds (e.g., MA crossovers, ATR percentiles). They are not machine-learning models and can lag sudden market shifts.
- **Universe Dependency**: The cross-sectional map is highly sensitive to the universe provided. A small or biased universe will yield inaccurate breadth and dispersion metrics.
- **Sector Proxy limits**: Without a paid sector classification API, sector dispersion is either limited to locally available metadata or defaults to symbol-level dispersion.
- **Breadth Proxy limits**: This uses internal symbol data to proxy breadth; it is not a direct replacement for official exchange breadth feeds (like NYSE TICK or TRIN).
- **Transition Risk is not Certainty**: A detected transition is a risk warning, not a guaranteed market prediction.
- **No Live Trading**: A 'PASS' or 'CONFIRMED' status from the regime map is purely for local analytics. It is **NOT** a live trading approval.
- **No Broker Integration**: This system does not route orders, use broker SDKs, or execute live trades.
- **Not Investment Advice**: The output of the regime map and its associated warnings are for research and software testing only.
