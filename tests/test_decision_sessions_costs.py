from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from usa_signal_bot.decision import DecisionConfig
from usa_signal_bot.decision.cost_capacity import cost_capacity_grid, impact_bps
from usa_signal_bot.decision.sessions import NY, early_close_days, is_regular_session, is_trading_day, session_bounds
from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.universe import PointInTimeUniverse


def _utc(bounds):
    return tuple(b.astimezone(timezone.utc).strftime("%H:%M") for b in bounds)


def test_open_close_in_utc_across_dst_transitions():
    # US DST 2026: starts Sun 2026-03-08, ends Sun 2026-11-01
    assert _utc(session_bounds(date(2026, 3, 6))) == ("14:30", "21:00")  # EST (UTC-5)
    assert _utc(session_bounds(date(2026, 3, 9))) == ("13:30", "20:00")  # EDT (UTC-4)
    assert _utc(session_bounds(date(2026, 10, 30))) == ("13:30", "20:00")
    assert _utc(session_bounds(date(2026, 11, 2))) == ("14:30", "21:00")
    assert session_bounds(date(2026, 3, 8)) is None  # Sunday


def test_half_days_close_at_1300_local():
    for d in (date(2025, 11, 28), date(2026, 11, 27), date(2026, 12, 24), date(2025, 7, 3)):
        assert d in early_close_days(d.year)
        assert session_bounds(d)[1].astimezone(NY).strftime("%H:%M") == "13:00"
    # 2026-07-03 is the observed Independence Day holiday (July 4 is a Saturday): closed, not a half day
    assert not is_trading_day(date(2026, 7, 3)) and session_bounds(date(2026, 7, 3)) is None
    # Dec 24 2027 is a Friday-observed Christmas holiday week: Dec 24 is a holiday, no half day
    assert not is_trading_day(date(2027, 12, 24))


def test_half_day_afternoon_is_outside_regular_session():
    inside = datetime(2026, 11, 27, 12, 59, tzinfo=NY)
    after = datetime(2026, 11, 27, 13, 0, tzinfo=NY)
    assert is_regular_session(inside) and not is_regular_session(after)


def test_utc_timestamp_respects_dst_offset():
    # 13:30 UTC is the open in summer, but only pre-market in winter
    assert is_regular_session(datetime(2026, 7, 15, 13, 30, tzinfo=timezone.utc))
    assert not is_regular_session(datetime(2026, 1, 15, 13, 30, tzinfo=timezone.utc))
    assert is_regular_session(datetime(2026, 1, 15, 14, 30, tzinfo=timezone.utc))


def test_session_length_regular_vs_half_day():
    o, c = session_bounds(date(2026, 6, 10))
    assert c - o == timedelta(hours=6, minutes=30)
    o, c = session_bounds(date(2026, 11, 27))
    assert c - o == timedelta(hours=3, minutes=30)


def test_impact_grows_with_size():
    assert impact_bps(1e6, 5e7) < impact_bps(1e7, 5e7)
    assert impact_bps(0, 5e7) == 0.0
    with pytest.raises(ValueError):
        impact_bps(1.0, 0.0)


def test_cost_capacity_grid_is_deterministic_and_higher_cost_hurts():
    data = synthetic_market(seed=3, n_symbols=10, n_days=500)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    kw = dict(capitals=(1e5, 1e7), slippage_bps=(2.0, 40.0))
    g1 = cost_capacity_grid(data.prices, members, DecisionConfig(), **kw)
    g2 = cost_capacity_grid(data.prices, members, DecisionConfig(), **kw)
    assert g1 == g2 and len(g1) == 4
    by = {(p.capital, p.slippage_bps): p for p in g1}
    assert by[(1e5, 40.0)].total_return < by[(1e5, 2.0)].total_return
    assert by[(1e7, 2.0)].effective_slippage_bps > by[(1e5, 2.0)].effective_slippage_bps
