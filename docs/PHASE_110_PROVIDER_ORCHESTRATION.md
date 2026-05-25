# Phase 110: Provider Orchestration

## Overview
Phase 110 builds the provider orchestration layer. It ingests the read-only Provider Quality Full Review from Phase 109 and builds route plans and source blending requests.

## Route Plans & Results
- **ProviderRoutePlan**: Determines candidate providers based on quality scores.
- **ProviderRouteResult**: The final selected path. Crucially, a route output is **NOT** a trade signal or an investment recommendation. It only identifies where research data should be pulled from.

## Commands
```bash
python -m usa_signal_bot provider-orchestration-info
python -m usa_signal_bot provider-route-plan
python -m usa_signal_bot provider-orchestration-review --write
```
