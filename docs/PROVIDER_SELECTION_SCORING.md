# Provider Selection Scoring and Ranking

## Overview
Provider Selection Scores balance data quality, trust profiles, and availability to determine the best local data source for research simulations.

## Ranking Engine
The engine processes all selection scores and emits a `ProviderRanking` assigning a `preferred_provider` and `fallback_providers`.

## Limitations
- Explicitly enforces `ranking_is_research_data_only = True`.
- Preferred providers are selected ONLY for data sourcing preference, not strategy execution.
