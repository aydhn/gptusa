import pytest
from datetime import datetime, timezone

from usa_signal_bot.core.enums import SymbolReadinessStatus, UniverseReadinessGateStatus, DataReadinessStatus
from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol, AssetType
from usa_signal_bot.data.readiness import DataReadinessReport, DataReadinessItem
from usa_signal_bot.universe.readiness_gate import (
    default_universe_readiness_gate_criteria,
    evaluate_universe_readiness_gate,
    get_eligible_symbols,
    get_ineligible_symbols,
    assert_universe_readiness_gate_passed,
    UniverseReadinessGateError
)

def test_gate_criteria_default():
    crit = default_universe_readiness_gate_criteria()
    assert crit.min_symbol_score == 70.0
    assert crit.required_primary_timeframe == "1d"

def test_evaluate_gate_passed():
    uni = UniverseDefinition(name="test", symbols=[
        UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK, active=True),
        UniverseSymbol(symbol="MSFT", asset_type=AssetType.STOCK, active=True)
    ])

    rep = DataReadinessReport(
        report_id="test", created_at_utc=datetime.now(timezone.utc).isoformat(),
        timeframes=["1d", "1h"],
        items=[
            DataReadinessItem(symbol="AAPL", timeframe="1d", status=DataReadinessStatus.READY),
            DataReadinessItem(symbol="AAPL", timeframe="1h", status=DataReadinessStatus.READY),
            DataReadinessItem(symbol="MSFT", timeframe="1d", status=DataReadinessStatus.READY),
            DataReadinessItem(symbol="MSFT", timeframe="1h", status=DataReadinessStatus.READY), # Partial
        ]
    )

    gate = evaluate_universe_readiness_gate(uni, rep)

    assert gate.status == UniverseReadinessGateStatus.PASSED
    assert gate.eligible_symbols == 2
    assert gate.partial_symbols == 0

    eligible = get_eligible_symbols(gate)
    assert "AAPL" in eligible
    assert "MSFT" in eligible # Partial is eligible

def test_evaluate_gate_failed_missing_primary():
    uni = UniverseDefinition(name="test", symbols=[
        UniverseSymbol(symbol="AAPL", asset_type=AssetType.STOCK, active=True),
    ])

    rep = DataReadinessReport(
        report_id="test", created_at_utc=datetime.now(timezone.utc).isoformat(),
        timeframes=["1d", "1h"],
        items=[
            DataReadinessItem(symbol="AAPL", timeframe="1h", status=DataReadinessStatus.READY), # Has 1h, missing 1d
        ]
    )

    gate = evaluate_universe_readiness_gate(uni, rep)

    assert gate.status == UniverseReadinessGateStatus.FAILED
    assert gate.ineligible_symbols == 1
    assert gate.eligible_symbols == 0
    assert "AAPL" in get_ineligible_symbols(gate)

    with pytest.raises(UniverseReadinessGateError):
        assert_universe_readiness_gate_passed(gate)
