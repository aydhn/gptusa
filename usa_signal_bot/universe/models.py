from dataclasses import dataclass
from typing import Optional
from ..core.domain import BaseDomainModel
from ..core.enums import AssetType
from ..core.model_validation import ensure_non_empty_string, ensure_enum_value

@dataclass
class UniverseSymbol(BaseDomainModel):
    symbol: str = ""
    name: Optional[str] = None
    asset_type: AssetType = AssetType.STOCK
    exchange: Optional[str] = None
    currency: str = "USD"
    active: bool = True
    sector: Optional[str] = None
    industry: Optional[str] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_non_empty_string(self.symbol, "symbol")
        ensure_non_empty_string(self.currency, "currency")
        ensure_enum_value(self.asset_type, AssetType, "asset_type")

@dataclass
class UniverseDefinition(BaseDomainModel):
    name: str = ""
    symbols: list[UniverseSymbol] = None
    description: Optional[str] = None
    created_from: Optional[str] = None

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = []

    def get_active_symbols(self) -> list[str]:
        return [s.symbol for s in self.symbols if s.active]

    def count_by_asset_type(self) -> dict[str, int]:
        counts = {}
        for s in self.symbols:
            val = s.asset_type.value if hasattr(s.asset_type, 'value') else str(s.asset_type)
            counts[val] = counts.get(val, 0) + 1
        return counts

@dataclass
class UniverseFilter(BaseDomainModel):
    include_stocks: bool = True
    include_etfs: bool = True
    min_price: Optional[float] = None
    max_symbols: Optional[int] = None
