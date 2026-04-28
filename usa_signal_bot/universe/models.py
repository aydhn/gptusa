from dataclasses import dataclass, field
from typing import Optional, List, Dict
from usa_signal_bot.core.domain import BaseDomainModel
from usa_signal_bot.core.enums import AssetType
from usa_signal_bot.core.model_validation import ensure_non_empty_string, ensure_enum_value

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
    symbols: List[UniverseSymbol] = field(default_factory=list)
    description: Optional[str] = None
    created_from: Optional[str] = None

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = []

    def get_active_symbols(self) -> List[str]:
        return [s.symbol for s in self.symbols if s.active]

    def count_by_asset_type(self) -> Dict[str, int]:
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

@dataclass
class UniverseLoadResult(BaseDomainModel):
    universe: UniverseDefinition = field(default_factory=UniverseDefinition)
    source_path: str = ''
    row_count: int = 0
    valid_count: int = 0
    invalid_count: int = 0
    duplicate_count: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class UniverseValidationIssue(BaseDomainModel):
    field: str = ''
    severity: str = ''
    message: str = ''
    row_number: Optional[int] = None
    symbol: Optional[str] = None

@dataclass
class UniverseValidationReport(BaseDomainModel):
    source_path: str = ''
    passed: bool = False
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    duplicate_symbols: List[str] = field(default_factory=list)
    issues: List[UniverseValidationIssue] = field(default_factory=list)

@dataclass
class UniverseSummary(BaseDomainModel):
    name: str = ''
    total_symbols: int = 0
    active_symbols: int = 0
    stock_count: int = 0
    etf_count: int = 0
    inactive_count: int = 0
    exchanges: Dict[str, int] = field(default_factory=dict)
    sectors: Dict[str, int] = field(default_factory=dict)
    source_files: List[str] = field(default_factory=list)
