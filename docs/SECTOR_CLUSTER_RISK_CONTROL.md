# Sector & Cluster Risk Control

This module provides heuristics for tracking sector and cluster exposure without relying on external paid APIs or scraping.

## Registry
A local registry (`config/portfolio/sector_cluster_registry.example.json`) can be maintained manually.
The system uses heuristics (like "SPY" -> "broad_market") for common index ETFs.

## Example CLI Commands
```bash
python -m usa_signal_bot sector-cluster-write-example
python -m usa_signal_bot sector-cluster-resolve --symbol AAPL
```
