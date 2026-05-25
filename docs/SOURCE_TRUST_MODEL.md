# Source Trust Model

## Overview
The Source Trust Model evaluates the holistic reliability of a data provider across its lifecycle.

## Inputs
It derives the `SourceTrustProfile` from historical and current `ProviderDataQualityScore` metrics:
- Schema Reliability
- Freshness Reliability
- Agreement Reliability
- Cache Reliability
- Safety Reliability

## Notice
The resulting `trust_score` and `trust_level` are strictly data-quality metadata. They DO NOT constitute investment advice, trade signals, or broker routing endorsements.
