# Indicator Engine Foundation

Phase 13 establishes the foundational architecture for the technical indicator engine.

## Purpose

The Indicator Engine is designed to compute technical features from validated OHLCV data.
It operates strictly on offline cache or batch data, maintaining the project's constraint of never directly querying data providers or live broker routes.
At this stage, it produces pure technical series (features) without interpreting them into trade signals or generating strategy recommendations.

## Interface and Registry

- **`Indicator` Interface**: An abstract base class that all technical indicators must implement. It guarantees standardized `metadata`, `parameter_schema`, and a deterministic `compute` method.
- **`IndicatorRegistry`**: A central, in-memory repository tracking all available indicators. It prevents naming conflicts and allows dynamic querying of indicators by name or category.
- **Metadata & Parameter Schemas**: Each indicator exposes `IndicatorMetadata` defining its category, required columns, min bars, and output series. The `IndicatorParameterSchema` ensures inputs to the indicator are strictly validated against types, boundaries, and required states.

## Built-in Basic Indicators

This phase includes the following simple indicators to test the pipeline:
1. `close_return`: Percentage return over $n$ periods.
2. `close_sma`: Simple Moving Average of the close price.
3. `close_ema`: Exponential Moving Average of the close price.
4. `volume_sma`: Simple Moving Average of volume.
5. `rolling_high`: Rolling maximum of high prices.
6. `rolling_low`: Rolling minimum of low prices.

## CLI Commands

You can interact with the registry and metadata via the CLI:
```bash
python -m usa_signal_bot indicator-list
python -m usa_signal_bot indicator-info --name close_sma
```
