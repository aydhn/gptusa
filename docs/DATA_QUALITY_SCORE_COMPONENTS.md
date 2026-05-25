# Data Quality Score Components

The data quality score consists of 8 weighted components:

1. **Completeness (20%)**: Evaluates missing columns/rows.
2. **Freshness (15%)**: Evaluates staleness vs expected TTL.
3. **Schema Validity (20%)**: Checks type and structure compliance.
4. **Continuity (15%)**: Punishes timestamp gaps/drops.
5. **Source Agreement (15%)**: Evaluates divergence against other baseline providers.
6. **Outlier Profile (5%)**: Checks basic OHLCV constraints (e.g. low > high).
7. **Cache Reliability (5%)**: Values consistent cache status.
8. **Safety Compliance (5%)**: Evaluates presence of active execution flags (broker, network, mutations).

Any failure on Safety or Schema heavily penalizes the total score or outright BLOCKS the provider.
