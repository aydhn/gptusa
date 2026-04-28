from typing import Literal, Any

Symbol = str
Currency = str
TimeFrameValue = str
StrategyName = str
FeatureName = str
RegimeName = str
ModelName = str
PortfolioId = str
OrderId = str
TradeId = str
PositionId = str
EventId = str

Numeric = int | float
JsonDict = dict[str, Any]
JsonList = list[JsonDict]

AssetTypeLiteral = Literal["stock", "etf", "STOCK", "ETF"]
ExecutionMode = Literal["local_paper_only"]
