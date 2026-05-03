"""Signal risk flag assignment system."""

from dataclasses import dataclass
from typing import List

from usa_signal_bot.core.enums import SignalRiskFlag
from usa_signal_bot.strategies.signal_contract import StrategySignal

@dataclass
class SignalRiskFlagRule:
    name: str
    flag: SignalRiskFlag
    severity: str
    description: str

def default_signal_risk_flag_rules() -> List[SignalRiskFlagRule]:
    return [
        SignalRiskFlagRule(
            name="Missing Feature Snapshot",
            flag=SignalRiskFlag.INSUFFICIENT_FEATURES,
            severity="HIGH",
            description="The feature snapshot is empty."
        ),
        SignalRiskFlagRule(
            name="Missing Reasons",
            flag=SignalRiskFlag.STRATEGY_ERROR,
            severity="HIGH",
            description="No reasons were provided for the signal."
        ),
        SignalRiskFlagRule(
            name="Data Quality Warning",
            flag=SignalRiskFlag.DATA_QUALITY_WARNING,
            severity="MODERATE",
            description="The signal metadata contains a data quality warning."
        ),
        SignalRiskFlagRule(
            name="Low Liquidity",
            flag=SignalRiskFlag.LOW_LIQUIDITY,
            severity="MODERATE",
            description="The feature snapshot indicates low liquidity."
        ),
        SignalRiskFlagRule(
            name="High Volatility",
            flag=SignalRiskFlag.HIGH_VOLATILITY,
            severity="MODERATE",
            description="The feature snapshot indicates exceptionally high volatility."
        )
    ]

def assign_risk_flags(signal: StrategySignal) -> List[SignalRiskFlag]:
    flags = set()

    # 1. Missing feature snapshot
    if not signal.feature_snapshot:
        flags.add(SignalRiskFlag.INSUFFICIENT_FEATURES)

    # 2. Missing reasons
    if not signal.reasons:
        flags.add(SignalRiskFlag.STRATEGY_ERROR)

    # 3. Data quality warning in metadata
    if signal.metadata and signal.metadata.get("data_quality_warning", False):
        flags.add(SignalRiskFlag.DATA_QUALITY_WARNING)

    # 4. Low liquidity detection
    if signal.feature_snapshot:
        avg_volume = signal.feature_snapshot.get("avg_volume_20", signal.feature_snapshot.get("volume", float('inf')))
        if avg_volume < 500000:  # arbitrary threshold for local testing
            flags.add(SignalRiskFlag.LOW_LIQUIDITY)

    # 5. High volatility detection
    if signal.feature_snapshot:
        atr_pct = signal.feature_snapshot.get("atr_pct", 0)
        if atr_pct > 0.10: # >10% average daily move
            flags.add(SignalRiskFlag.HIGH_VOLATILITY)

    return list(flags)

def merge_risk_flags(existing: List[SignalRiskFlag], new_flags: List[SignalRiskFlag]) -> List[SignalRiskFlag]:
    merged = set(existing)
    merged.update(new_flags)
    return list(merged)

def risk_flags_to_text(flags: List[SignalRiskFlag]) -> str:
    if not flags:
        return "None"
    return ", ".join([f.value if hasattr(f, 'value') else str(f) for f in flags])

def has_high_risk_flags(flags: List[SignalRiskFlag]) -> bool:
    high_risk_flags = {
        SignalRiskFlag.STRATEGY_ERROR,
        SignalRiskFlag.INSUFFICIENT_FEATURES,
        SignalRiskFlag.CONFLICTING_FEATURES
    }
    return any(f in high_risk_flags for f in flags)
