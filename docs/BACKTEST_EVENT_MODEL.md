# Backtest Event Model

The backtesting framework uses an event-driven architecture to model historical simulations deterministically. The engine processes a unified, time-sorted stream of events.

## Event Types (`BacktestEventType`)
1. **MARKET_BAR**: Represents a new market data point (`OHLCVBar`). This updates the current market prices and allows the portfolio to mark-to-market.
2. **SIGNAL**: Represents a generated `StrategySignal`. The engine evaluates these to generate `ORDER_INTENT`s.
3. **ORDER_INTENT**: A declared intention to place a trade (e.g., BUY, SELL).
4. **FILL**: A simulated execution of an `ORDER_INTENT`. Updates cash and positions.
5. **POSITION_UPDATE**: Reflects changes in position sizing or PnL.
6. **PORTFOLIO_SNAPSHOT**: Recorded at the end of each `MARKET_BAR` to track equity curve progression.
7. **EQUITY_UPDATE**: Used to construct the final equity curve model.

## Deterministic Ordering
All events are processed in chronological order (`timestamp_utc`). If multiple events share a timestamp, they are processed by a strict `sequence` integer hierarchy:
* Market events (`sequence=0`) happen first to establish price contexts.
* Signal events (`sequence=10`) happen subsequently.

This model is an internal research construct and **does not** represent a live execution router or broker integration.
