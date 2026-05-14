
# Cost Robustness Limitations

1. **Heuristic Nature**: Stress scenarios are multipliers applied to estimated costs. They do not simulate actual market microstructure.
2. **No Order Book**: We do not replay Level 2 data.
3. **No Broker Fill Data**: We do not use live or demo accounts to verify fills.
4. **No Real Fee Schedules**: Fee stress uses proxies, not exact broker tiered schedules.
5. **Not Investment Advice**: A PASS status is an operational gate, NOT a live trading recommendation.
6. **No External Tools**: Strictly standard library and pandas.
