# Prediction Output Boundary

## Overview
Enforces that model outputs only generate theoretical, research-oriented schema columns.

## Allowed Outputs
- `RESEARCH_SCORE_ONLY`
- `RESEARCH_PROBABILITY_ONLY`
- `RESEARCH_CLASS_LABEL_ONLY`
- `RESEARCH_REGRESSION_VALUE_ONLY`
- `DIAGNOSTIC_METADATA_ONLY`

## Forbidden Outputs
- `buy_signal`, `sell_signal`, `entry`, `exit`, `order`, `broker_order`, `portfolio_weight`, `allocation`, etc.
