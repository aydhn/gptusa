import json

import numpy as np
import pandas as pd

from usa_signal_bot.decision.pipeline import Decision
from usa_signal_bot.decision.reporting import (
    RiskBudget, daily_active_report, explain_positions, latest_evidence_note, weekly_summary, write_decision_journal,
)


def _daily():
    idx = pd.bdate_range("2021-01-04", periods=200)
    rng = np.random.default_rng(0)
    eq = pd.Series(100000 * np.cumprod(1 + rng.normal(0.0004, 0.01, 200)), index=idx)
    bench = pd.Series(rng.normal(0.0004, 0.01, 200), index=idx)
    return daily_active_report(eq, bench, 0.02, 0.025, RiskBudget(0.04, 0.2))


def test_daily_active_report_columns_and_budget():
    d = _daily()
    assert {"tracking_error", "risk_budget_used", "cash_rate_annual", "real_equity_index", "cum_active"} <= set(d.columns)
    assert abs(d["risk_budget_used"].dropna().iloc[-1] - d["tracking_error"].dropna().iloc[-1] / 0.04) < 1e-12


def test_weekly_summary_mentions_cash_interest_real_and_evidence():
    md = weekly_summary(_daily(), 0.025, "kanıt yok", interest_earned=12.5)
    assert "reel" in md and "nakit faizi" in md and "kanıt yok" in md and "yatırım tavsiyesi değildir" in md


def test_why_positions_and_journal(tmp_path):
    dec = Decision("RISK_ON", 0.9, {"A": 0.5, "B": 0.4}, {"C": "stop"}, ["REGIME RISK_ON"])
    md = explain_positions(dec, {"A": 0.3, "B": 0.2, "C": -0.1}, {"A": 0.01})
    assert "| A |" in md and "REGIME RISK_ON" in md
    p = tmp_path / "j.jsonl"
    assert write_decision_journal([dec], [pd.Timestamp("2021-01-04")], p) == 1
    assert json.loads(p.read_text(encoding="utf-8"))["exits"] == {"C": "stop"}


def test_latest_evidence_note_default_and_read(tmp_path):
    assert "edge" in latest_evidence_note(None)
    f = tmp_path / "r.md"
    f.write_text("x\n**Sonuç:** edge yok\n", encoding="utf-8")
    assert latest_evidence_note(f) == "Sonuç: edge yok"
