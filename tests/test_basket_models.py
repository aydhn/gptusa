import pytest
from usa_signal_bot.backtesting.basket_models import (
    BasketReplayRequest, BasketSimulationConfig, BasketReplayItem, BasketExposureSnapshot, BasketSimulationResult,
    create_basket_replay_request_id, create_basket_simulation_run_id,
    validate_basket_replay_request, validate_basket_simulation_config, validate_basket_replay_item,
    basket_replay_request_to_dict, basket_simulation_config_to_dict, basket_replay_item_to_dict,
    basket_exposure_snapshot_to_dict, basket_simulation_result_to_dict, BasketReplayData, basket_replay_data_to_dict
)
from usa_signal_bot.core.enums import BasketReplaySource, BasketEntryMode, BasketExitMode, AllocationReplayMode, SignalAction, BasketSimulationStatus, BasketReviewStatus
from usa_signal_bot.core.exceptions import BasketValidationError
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolio

def test_basket_replay_request_valid():
    req = BasketReplayRequest(
        request_id="req1",
        source=BasketReplaySource.PORTFOLIO_BASKET,
        basket_file="basket.json",
        timeframe="1d"
    )
    assert req.request_id == "req1"
    validate_basket_replay_request(req)

def test_basket_replay_request_invalid_source():
    req = BasketReplayRequest(
        request_id="req1",
        source=BasketReplaySource.PORTFOLIO_BASKET,
        timeframe="1d"
    )
    with pytest.raises(BasketValidationError, match="basket_file required"):
        validate_basket_replay_request(req)

def test_basket_simulation_config_valid():
    cfg = BasketSimulationConfig(
        starting_cash=1000.0,
        entry_mode=BasketEntryMode.ENTER_ALL_AT_START,
        exit_mode=BasketExitMode.HOLD_N_BARS,
        allocation_replay_mode=AllocationReplayMode.TARGET_NOTIONAL,
        hold_bars=5,
        allow_fractional_quantity=True,
        prevent_same_bar_fill=True,
        max_positions=20,
        max_total_allocation_pct=0.8
    )
    validate_basket_simulation_config(cfg)

def test_basket_simulation_config_invalid():
    cfg = BasketSimulationConfig(
        starting_cash=-1000.0,
        entry_mode=BasketEntryMode.ENTER_ALL_AT_START,
        exit_mode=BasketExitMode.HOLD_N_BARS,
        allocation_replay_mode=AllocationReplayMode.TARGET_NOTIONAL,
        hold_bars=5,
        allow_fractional_quantity=True,
        prevent_same_bar_fill=True,
        max_positions=20,
        max_total_allocation_pct=0.8
    )
    with pytest.raises(BasketValidationError, match="positive"):
        validate_basket_simulation_config(cfg)

def test_basket_replay_item_valid():
    item = BasketReplayItem(
        item_id="item1",
        candidate_id=None,
        signal_id=None,
        symbol="AAPL",
        timeframe="1d",
        strategy_name=None,
        action=SignalAction.LONG,
        target_weight=0.5,
        target_notional=None,
        target_quantity=None,
        rank_score=None,
        risk_score=None,
        confidence=None,
        timestamp_utc="2023-01-01T00:00:00"
    )
    validate_basket_replay_item(item)

def test_basket_replay_item_invalid_weight():
    item = BasketReplayItem(
        item_id="item1",
        candidate_id=None,
        signal_id=None,
        symbol="AAPL",
        timeframe="1d",
        strategy_name=None,
        action=SignalAction.LONG,
        target_weight=1.5,
        target_notional=None,
        target_quantity=None,
        rank_score=None,
        risk_score=None,
        confidence=None,
        timestamp_utc="2023-01-01T00:00:00"
    )
    with pytest.raises(BasketValidationError, match="between 0 and 1"):
        validate_basket_replay_item(item)

def test_serialize():
    req = BasketReplayRequest("r1", BasketReplaySource.SIGNALS, signal_file="sig.json")
    d = basket_replay_request_to_dict(req)
    assert d["request_id"] == "r1"

    cfg = BasketSimulationConfig(100.0, BasketEntryMode.ENTER_ALL_AT_START, BasketExitMode.HOLD_N_BARS, AllocationReplayMode.TARGET_NOTIONAL, 5, True, True, 20, 0.8)
    d = basket_simulation_config_to_dict(cfg)
    assert d["starting_cash"] == 100.0

    item = BasketReplayItem("i1", None, None, "AAPL", "1d", None, SignalAction.LONG, 0.5, None, None, None, None, None, None)
    d = basket_replay_item_to_dict(item)
    assert d["target_weight"] == 0.5

    data = BasketReplayData(req, [item], ["AAPL"], "1d", [], [])
    d = basket_replay_data_to_dict(data)
    assert len(d["items"]) == 1

    snap = BasketExposureSnapshot("2023", 100, 50, 50, 50, 0.5, 0.5, {"AAPL": 0.5}, {"AAPL": 0.5}, {"AAPL": 0.0}, 1)
    d = basket_exposure_snapshot_to_dict(snap)
    assert d["equity"] == 100

    res = BasketSimulationResult(
        run_id="run1",
        created_at_utc="2023",
        status=BasketSimulationStatus.COMPLETED,
        request=req,
        config=cfg,
        replay_data=data,
        portfolio=BacktestPortfolio(100.0, 100.0, {}, 0.0, 0.0, 100.0, '2023'),
        snapshots=[],
        basket_exposure_snapshots=[snap],
        order_intents=[],
        fills=[],
        trade_ledger=None,
        basket_metrics={"a": 1},
        benchmark_summary={},
        review_status=BasketReviewStatus.ACCEPTABLE,
        warnings=[],
        errors=[]
    )
    d = basket_simulation_result_to_dict(res)
    assert d["run_id"] == "run1"

def test_factories():
    r1 = create_basket_replay_request_id()
    assert r1.startswith("basket_replay_")
    assert len(r1) > 15
    r2 = create_basket_simulation_run_id()
    assert r2.startswith("basket_sim_")
