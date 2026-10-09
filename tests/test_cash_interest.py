import pandas as pd
import pytest

from usa_signal_bot.decision.ledger import PaperLedger
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.rates import align_rate, daily_from_annual, load_rate_csv, real_cagr, yoy_inflation_from_index
from usa_signal_bot.evidence.walk_forward import backtest_weights


def _flat(n=252):
    idx = pd.bdate_range("2020-01-01", periods=n)
    returns = pd.DataFrame({"A": 0.0}, index=idx)
    return idx, returns


def test_all_cash_earns_the_cash_rate_over_a_year():
    idx, returns = _flat(253)
    w = pd.DataFrame({"A": 0.0}, index=idx)
    net, _ = backtest_weights(w, returns, CostModel(0, 0), cash_rate=0.04)
    assert (1 + net).prod() - 1 == pytest.approx(0.04, abs=2e-4)  # 252 daily accruals of a 4% annual rate
    net0, _ = backtest_weights(w, returns, CostModel(0, 0), cash_rate=0.0)
    assert net0.sum() == 0.0


def test_only_the_uninvested_fraction_earns_interest():
    idx, returns = _flat(10)
    w = pd.DataFrame({"A": 0.6}, index=idx)
    net, _ = backtest_weights(w, returns, CostModel(0, 0), cash_rate=0.05)
    assert net.iloc[-1] == pytest.approx(0.4 * float(daily_from_annual(pd.Series([0.05])).iloc[0]))
    w_full = pd.DataFrame({"A": 1.0}, index=idx)
    assert backtest_weights(w_full, returns, CostModel(0, 0), cash_rate=0.05)[0].iloc[-1] == 0.0


def test_rate_series_is_forward_filled_without_lookahead():
    idx = pd.bdate_range("2020-01-01", periods=10)
    s = pd.Series([0.01, 0.03], index=[idx[0], idx[5]])
    a = align_rate(s, idx)
    assert a.iloc[4] == 0.01 and a.iloc[5] == 0.03 and a.iloc[9] == 0.03
    assert align_rate(s, idx[:3]).eq(0.01).all()


def test_load_rate_csv_and_real_cagr(tmp_path):
    p = tmp_path / "dtb3.csv"
    p.write_text("DATE,DTB3\n2020-01-01,1.5\n2020-01-02,.\n2020-01-03,2.0\n", encoding="utf-8")
    s = load_rate_csv(p)
    assert list(s.round(4)) == [0.015, 0.02]
    assert real_cagr(0.05, 0.025) == pytest.approx(1.05 / 1.025 - 1)
    cpi = pd.Series(range(100, 124), index=pd.date_range("2020-01-31", periods=24, freq="ME"), dtype=float)
    assert yoy_inflation_from_index(cpi).iloc[0] == pytest.approx(112 / 100 - 1)


def test_ledger_accrues_interest_on_idle_cash_by_calendar_days():
    led = PaperLedger(initial_cash=100_000.0, cash_rate_annual=0.05)
    assert led.accrue_interest("2026-01-02") == 0.0  # first call only sets the clock
    gained = led.accrue_interest("2026-01-05")  # 3 calendar days over a weekend
    assert gained == pytest.approx(100_000.0 * (1.05 ** (3 / 365) - 1))
    assert led.cash == pytest.approx(100_000.0 + gained) and led.interest_earned == pytest.approx(gained)
    led.accrue_interest("2026-01-05")  # same day: nothing
    assert led.interest_earned == pytest.approx(gained)
    off = PaperLedger(initial_cash=100_000.0)  # default rate 0: unchanged behaviour
    off.accrue_interest("2026-01-02"); off.accrue_interest("2026-02-02")
    assert off.cash == 100_000.0
