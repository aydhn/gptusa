from datetime import date

import pandas as pd
import pytest

from usa_signal_bot.decision.package import build_package, hypothesis_summary
from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.evidence.hypothesis_log import HypothesisLog
from usa_signal_bot.evidence.universe import PointInTimeUniverse

DISC = "yatırım tavsiyesi değildir"


@pytest.fixture(scope="module")
def market():
    d = synthetic_market(seed=5, n_symbols=12, n_days=600)
    return d.prices, PointInTimeUniverse.from_frame(d.memberships).membership_matrix(d.prices.index, d.prices.columns)


def _log(tmp_path):
    h = HypothesisLog(tmp_path / "h.jsonl", clock=lambda: "t")
    h.append("r1", "momentum", {"lb": 126}, 500, 0.05, "syn")
    h.append("r1", "momentum", {"lb": 63}, 500, 0.02, "syn")
    h.append("r1", "lowvol", {"w": 60}, 500, 0.01, "syn")
    return tmp_path / "h.jsonl"


def test_hypothesis_summary(tmp_path):
    s = hypothesis_summary(_log(tmp_path))
    assert s["n_trials"] == 3 and set(s["families"]) == {"momentum", "lowvol"}
    assert s["families"]["momentum"]["best_sharpe"] > s["families"]["lowvol"]["best_sharpe"]
    assert hypothesis_summary(tmp_path / "missing.jsonl")["n_trials"] == 0


def test_package_files_and_disclaimer(tmp_path, market):
    prices, members = market
    out = build_package(prices, members, tmp_path / "pk", as_of="2026-10-10", hypothesis_log=_log(tmp_path), inflation=0.03,
                        clock=lambda: date(2026, 1, 1))
    assert out.name == "2026-10-10"
    names = {p.name for p in out.iterdir()}
    assert {"decision_journal.jsonl", "daily_active_risk.csv", "why_positions.md", "hypothesis_summary.md",
            "real_returns_cash.md", "weekly_summary.md"} <= names
    assert all(p.suffix in {".md", ".csv", ".jsonl"} for p in out.iterdir())
    for p in out.iterdir():
        assert DISC in p.read_text(encoding="utf-8"), p.name
    df = pd.read_csv(out / "daily_active_risk.csv", comment="#")
    assert {"active_ret", "risk_budget_used", "real_equity_index", "cash_rate_annual"} <= set(df.columns)
    assert "momentum" in (out / "hypothesis_summary.md").read_text(encoding="utf-8")
    assert "reel CAGR" in (out / "real_returns_cash.md").read_text(encoding="utf-8")


def test_package_default_date_from_injected_clock(tmp_path, market):
    prices, members = market
    out = build_package(prices, members, tmp_path / "pk", clock=lambda: date(2026, 3, 4))
    assert out.name == "2026-03-04"
