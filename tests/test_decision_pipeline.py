from datetime import date, datetime, timezone

import pandas as pd
import pytest

from usa_signal_bot.decision import DecisionConfig, ExitRules, PaperLedger, RiskLimits, decide
from usa_signal_bot.decision import ledger as ledger_module
from usa_signal_bot.decision.regime import NEUTRAL, RISK_OFF, RISK_ON, classify_regime
from usa_signal_bot.decision.rules import PositionState, apply_risk_limits, evaluate_exits, inverse_vol_weights
from usa_signal_bot.decision.sessions import (
    NY,
    early_close_days,
    easter,
    is_regular_session,
    is_trading_day,
    nyse_holidays,
    regular_session_mask,
    session_bounds,
)
from usa_signal_bot.decision.simulate import simulate_paper
from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.universe import PointInTimeUniverse


# ---- sessions / time zones -------------------------------------------------------------------
def test_easter_and_good_friday():
    assert easter(2026) == date(2026, 4, 5)
    assert nyse_holidays(2026)[date(2026, 4, 3)] == "Good Friday"


def test_2026_holidays_and_observance():
    hol = nyse_holidays(2026)
    assert date(2026, 7, 3) in hol  # July 4 is a Saturday -> observed Friday
    assert date(2026, 11, 26) in hol  # Thanksgiving
    assert date(2026, 12, 25) in hol
    assert date(2026, 6, 19) in hol  # Juneteenth
    assert not is_trading_day(date(2026, 1, 19))  # MLK
    assert is_trading_day(date(2026, 1, 20))


def test_new_year_on_saturday_is_not_observed_on_prior_year():
    assert date(2021, 12, 31) not in nyse_holidays(2021)  # Jan 1 2022 is a Saturday
    assert date(2022, 1, 1) not in nyse_holidays(2022)


def test_early_closes():
    assert date(2026, 11, 27) in early_close_days(2026)
    assert date(2026, 12, 24) in early_close_days(2026)
    assert date(2025, 7, 3) in early_close_days(2025)
    open_, close = session_bounds(date(2026, 11, 27))
    assert close.hour == 13 and open_.hour == 9 and open_.minute == 30


def test_dst_shifts_utc_boundary():
    winter = session_bounds(date(2026, 3, 6))[0].astimezone(timezone.utc)
    summer = session_bounds(date(2026, 3, 9))[0].astimezone(timezone.utc)
    assert winter.hour == 14 and summer.hour == 13  # 09:30 NY = 14:30Z (EST) / 13:30Z (EDT)


def test_is_regular_session_boundaries_and_naive_rejection():
    assert is_regular_session(datetime(2026, 3, 9, 13, 30, tzinfo=timezone.utc))  # 09:30 EDT
    assert not is_regular_session(datetime(2026, 3, 9, 13, 29, tzinfo=timezone.utc))
    assert not is_regular_session(datetime(2026, 3, 9, 20, 0, tzinfo=timezone.utc))  # 16:00 close is exclusive
    assert not is_regular_session(datetime(2026, 4, 3, 15, 0, tzinfo=timezone.utc))  # Good Friday
    with pytest.raises(ValueError):
        is_regular_session(datetime(2026, 3, 9, 10, 0))


def test_regular_session_mask_filters_premarket_and_holiday():
    idx = pd.DatetimeIndex(
        [
            pd.Timestamp("2026-03-09 08:00", tz=NY),
            pd.Timestamp("2026-03-09 09:30", tz=NY),
            pd.Timestamp("2026-03-09 15:59", tz=NY),
            pd.Timestamp("2026-03-09 16:00", tz=NY),
            pd.Timestamp("2026-04-03 10:00", tz=NY),
        ]
    )
    assert regular_session_mask(idx).tolist() == [False, True, True, False, False]


# ---- regime / rules ---------------------------------------------------------------------------
def test_regime_has_no_lookahead_and_labels():
    s = pd.Series(range(1, 700), index=pd.bdate_range("2018-01-01", periods=699), dtype=float)
    r = classify_regime(s)
    r2 = classify_regime(pd.concat([s.iloc[:500], s.iloc[500:] * 0.2]))
    assert r.iloc[:500].tolist() == r2.iloc[:500].tolist()
    assert set(r.unique()) <= {RISK_ON, NEUTRAL, RISK_OFF}


def test_exits():
    pos = {"A": PositionState(10, 100.0, 120.0, 0), "B": PositionState(10, 100.0, 100.0, 0), "C": PositionState(5, 50.0, 50.0, 0)}
    rules = ExitRules(stop_loss=0.10, trailing_stop=0.15, max_hold_days=30)
    out = evaluate_exits(pos, {"A": 100.0, "B": 89.0, "C": 50.0}, 31, RISK_ON, rules)
    assert out == {"A": "TRAILING_STOP", "B": "STOP_LOSS", "C": "MAX_HOLD"}
    assert evaluate_exits({"C": pos["C"]}, {"C": 50.0}, 1, RISK_OFF, rules) == {"C": "REGIME_RISK_OFF"}


def test_inverse_vol_weights_respect_cap_and_gross():
    w = inverse_vol_weights({"A": 0.01, "B": 0.02, "C": 0.04}, gross=1.0, max_weight=0.5)
    assert abs(sum(w.values()) - 1.0) < 1e-9
    assert max(w.values()) <= 0.5 + 1e-9
    assert w["A"] >= w["B"] >= w["C"]


def test_risk_limits_kill_switch_and_caps():
    limits = RiskLimits(max_positions=2, max_weight=0.4, max_gross=0.7, max_daily_turnover=10.0, drawdown_kill=0.2)
    w, why = apply_risk_limits({"A": 0.5, "B": 0.4, "C": 0.3}, {}, 0.0, limits)
    assert len(w) == 2 and sum(w.values()) <= 0.7 + 1e-9 and "MAX_POSITIONS" in why
    flat, why2 = apply_risk_limits({"A": 0.5}, {"A": 0.3}, -0.25, limits)
    assert flat == {} and why2[0].startswith("KILL_SWITCH")
    capped, why3 = apply_risk_limits({"A": 0.4}, {}, 0.0, RiskLimits(max_daily_turnover=0.1))
    assert abs(capped["A"] - 0.1) < 1e-9 and "TURNOVER_CAP" in why3


# ---- ledger -----------------------------------------------------------------------------------
def test_ledger_never_negative_cash_no_leverage_and_marks_local_only(tmp_path):
    assert ledger_module.ORDER_ROUTING_ENABLED is False
    assert ledger_module.EXECUTION_MODE == "local_paper_only"
    led = PaperLedger(initial_cash=10_000.0, journal_path=tmp_path / "fills.jsonl")
    led.rebalance_to({"A": 0.9, "B": 0.9}, {"A": 10.0, "B": 20.0}, "2026-01-02", 0)  # asks for 180% gross
    led.check_invariants()
    assert led.cash >= -1e-6
    assert (tmp_path / "fills.jsonl").read_text().count("local_paper_only") == len(led.fills)
    led.rebalance_to({}, {"A": 10.0, "B": 20.0}, "2026-01-03", 1)
    assert led.positions == {} and led.cash < 10_000.0  # costs were charged


# ---- end-to-end ------------------------------------------------------------------------------
def _sim(seed):
    data = synthetic_market(seed=seed, n_symbols=12, n_days=700)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    led = PaperLedger(initial_cash=100_000.0)
    decide_log = simulate_paper(data.prices, members, DecisionConfig(), led)
    return led, decide_log


def test_simulation_is_deterministic_and_respects_limits():
    led1, d1 = _sim(5)
    led2, d2 = _sim(5)
    assert led1.equity_curve == led2.equity_curve
    assert len(led1.fills) == len(led2.fills) > 0
    limits = DecisionConfig().limits
    for d in d1:
        assert sum(d.target_weights.values()) <= limits.max_gross + 1e-9
        assert all(w <= limits.max_weight + 1e-9 for w in d.target_weights.values())
        assert len(d.target_weights) <= limits.max_positions
    assert all(f.side in {"BUY", "SELL"} for f in led1.fills)
    led1.check_invariants()
