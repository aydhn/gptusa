# Source Blending

## Overview
Source blending takes records from multiple providers and merges them using methods like TRUST_WEIGHTED_BLEND.

## Rules
- Blending only generates research data preparation metadata.
- It **does not** generate buy/sell recommendations or execution intent.
- `produces_trade_signal` and `produces_order_decision` are strictly enforced as `False`.
