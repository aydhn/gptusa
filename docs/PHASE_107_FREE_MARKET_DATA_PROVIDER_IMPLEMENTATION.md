# Phase 107 - Free Market Data Provider Implementation

This phase implements free market data provider adapters with cache-aware fetch dry-run capabilities and provider contract tests.

## Goals
- Read-only ingestion of Phase 106 ProviderAbstractionFullReview.
- Transform skeleton adapters into real contract implementations (yfinance, stooq, local CSV).
- Create cache-aware dry-run fetch infrastructure.
- Network fetch is default off.

## Safety Constraints
- NO active paper trading.
- NO broker execution.
- NO HTML parsing.
- NO scraping.
- NO paid APIs.
- NO paper state mutation.

## Usage

Check runtime info:
`python -m usa_signal_bot provider-runtime-info`

Check registry:
`python -m usa_signal_bot provider-runtime-registry`

Run contract tests:
`python -m usa_signal_bot provider-contract-tests`
