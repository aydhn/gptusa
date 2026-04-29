from dataclasses import dataclass, field
from typing import Any, List, Optional
from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.core.enums import ValidationSeverity

@dataclass
class ValidationRuleResult:
    rule_name: str
    passed: bool
    severity: ValidationSeverity
    message: str
    symbol: Optional[str] = None
    timestamp_utc: Optional[str] = None
    field: Optional[str] = None
    details: dict = __import__("dataclasses").field(default_factory=dict)

def validate_required_ohlcv_fields(bar: OHLCVBar) -> List[ValidationRuleResult]:
    results = []
    if not bar.symbol:
        results.append(ValidationRuleResult("required_fields", False, ValidationSeverity.ERROR, "Symbol is required", field="symbol"))
    if not bar.timestamp_utc:
        results.append(ValidationRuleResult("required_fields", False, ValidationSeverity.ERROR, "Timestamp is required", symbol=bar.symbol, field="timestamp_utc"))
    return results

def validate_price_consistency(bar: OHLCVBar) -> List[ValidationRuleResult]:
    results = []
    if bar.open <= 0 or bar.high <= 0 or bar.low <= 0 or bar.close <= 0:
        results.append(ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "Prices must be positive", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="price"))
    if bar.high < bar.low:
        results.append(ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "High cannot be less than low", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="high"))
    if bar.high < bar.open or bar.high < bar.close:
        results.append(ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "High must be >= open and close", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="high"))
    if bar.low > bar.open or bar.low > bar.close:
        results.append(ValidationRuleResult("price_consistency", False, ValidationSeverity.ERROR, "Low must be <= open and close", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="low"))
    return results

def validate_volume(bar: OHLCVBar, allow_zero_volume: bool = True) -> List[ValidationRuleResult]:
    results = []
    if bar.volume < 0:
        results.append(ValidationRuleResult("volume", False, ValidationSeverity.ERROR, "Volume cannot be negative", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="volume"))
    elif bar.volume == 0 and not allow_zero_volume:
         results.append(ValidationRuleResult("volume", False, ValidationSeverity.WARNING, "Zero volume", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="volume"))
    elif bar.volume == 0 and allow_zero_volume:
         results.append(ValidationRuleResult("volume", False, ValidationSeverity.WARNING, "Zero volume", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="volume")) # still emit warning but handled upstream maybe? Spec says "zero volume default warning"
    return results

def validate_timestamp(bar: OHLCVBar) -> List[ValidationRuleResult]:
    # Placeholder for more complex timestamp rules if needed
    return []

def validate_symbol(bar: OHLCVBar, expected_symbols: Optional[List[str]] = None) -> List[ValidationRuleResult]:
    results = []
    if not bar.symbol:
         results.append(ValidationRuleResult("symbol", False, ValidationSeverity.ERROR, "Symbol is empty", field="symbol"))
    elif expected_symbols and bar.symbol not in expected_symbols:
         results.append(ValidationRuleResult("symbol", False, ValidationSeverity.WARNING, "Unexpected symbol", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="symbol"))
    return results

def validate_single_bar(bar: OHLCVBar, expected_symbols: Optional[List[str]] = None) -> List[ValidationRuleResult]:
    results = []
    results.extend(validate_required_ohlcv_fields(bar))
    results.extend(validate_price_consistency(bar))
    results.extend(validate_volume(bar))
    results.extend(validate_timestamp(bar))
    results.extend(validate_symbol(bar, expected_symbols))
    return results

def validate_bar_sequence(bars: List[OHLCVBar]) -> List[ValidationRuleResult]:
    results = []
    if not bars:
        return results

    # Sort bars by timestamp assuming same symbol for sequence check
    # Let's group by symbol first
    from collections import defaultdict
    by_sym = defaultdict(list)
    for b in bars:
        by_sym[b.symbol].append(b)

    for sym, sym_bars in by_sym.items():
        # check monotonic increasing
        for i in range(1, len(sym_bars)):
            if sym_bars[i].timestamp_utc < sym_bars[i-1].timestamp_utc:
                results.append(ValidationRuleResult("sequence", False, ValidationSeverity.WARNING, "Non-monotonic timestamp sequence", symbol=sym, timestamp_utc=sym_bars[i].timestamp_utc, field="timestamp_utc"))
                break # Just emit one warning per symbol
    return results

def validate_duplicate_bars(bars: List[OHLCVBar]) -> List[ValidationRuleResult]:
    results = []
    seen = set()
    for bar in bars:
        key = (bar.symbol, bar.timeframe, bar.timestamp_utc)
        if key in seen:
             results.append(ValidationRuleResult("duplicate", False, ValidationSeverity.ERROR, "Duplicate bar found", symbol=bar.symbol, timestamp_utc=bar.timestamp_utc, field="timestamp_utc"))
        else:
             seen.add(key)
    return results

def validate_missing_symbols(bars: List[OHLCVBar], expected_symbols: List[str]) -> List[ValidationRuleResult]:
    results = []
    found = set(b.symbol for b in bars)
    for sym in expected_symbols:
        if sym not in found:
            results.append(ValidationRuleResult("missing_symbol", False, ValidationSeverity.ERROR, "Missing expected symbol", symbol=sym, field="symbol"))
    return results

def validate_empty_dataset(bars: List[OHLCVBar]) -> List[ValidationRuleResult]:
    if not bars:
        return [ValidationRuleResult("empty_dataset", False, ValidationSeverity.ERROR, "Dataset is empty")]
    return []
