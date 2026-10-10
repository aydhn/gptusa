"""CLI: ``python -m usa_signal_bot decision-simulate`` (local simulated paper ledger, research only)."""

from __future__ import annotations

from pathlib import Path

from usa_signal_bot.decision.ledger import PaperLedger
from usa_signal_bot.decision.pipeline import DecisionConfig
from usa_signal_bot.decision.simulate import simulate_paper
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import load_csv_market, synthetic_market
from usa_signal_bot.evidence.metrics import summarize
from usa_signal_bot.evidence.universe import PointInTimeUniverse


def cmd_decision_simulate(args) -> None:
    data = load_csv_market(args.csv_dir, args.memberships) if args.source == "csv" else synthetic_market(seed=args.seed)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    journal = Path(args.journal) if args.journal else None
    ledger = PaperLedger(initial_cash=args.cash, cost=CostModel(args.commission_bps, args.slippage_bps), journal_path=journal, cash_rate_annual=args.cash_rate)
    decisions = simulate_paper(data.prices, members, DecisionConfig(), ledger)
    equity = __import__("pandas").Series(ledger.equity_curve)
    perf = summarize(equity.pct_change().dropna())
    print(f"Data: {data.label} | days={len(equity)} | fills={len(ledger.fills)} | decisions={len(decisions)}")
    print(f"Final equity: {equity.iloc[-1]:.2f} (start {args.cash:.2f}) | CAGR {perf.cagr:.1%} | Sharpe {perf.sharpe:.2f} | MaxDD {perf.max_drawdown:.1%}")
    print("Local simulated ledger only: no orders, no broker, not investment advice.")


def cmd_decision_report(args) -> None:
    """Simulate on the local ledger and write journal (JSONL), daily active-risk CSV, why-trace and weekly summary (MD)."""
    import pandas as pd

    from usa_signal_bot.decision.regime import classify_regime
    from usa_signal_bot.decision.reporting import (
        daily_active_report, explain_positions, latest_evidence_note, weekly_summary, write_decision_journal,
    )
    from usa_signal_bot.evidence.cli import _cash_rate, _inflation

    data = load_csv_market(args.csv_dir, args.memberships) if args.source == "csv" else synthetic_market(seed=args.seed)
    prices = data.prices
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(prices.index, prices.columns)
    cash = _cash_rate(args)
    ledger = PaperLedger(initial_cash=args.cash, cost=CostModel(args.commission_bps, args.slippage_bps),
                         cash_rate_annual=float(cash.iloc[-1]) if hasattr(cash, "iloc") else float(cash))
    decisions = simulate_paper(prices, members, DecisionConfig(), ledger)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_decision_journal(decisions, prices.index[: len(decisions)], out / "decision_journal.jsonl")
    bench = prices.pct_change(fill_method=None).where(members).mean(axis=1).fillna(0.0)
    inflation = _inflation(args, data)
    daily = daily_active_report(pd.Series(ledger.equity_curve), bench, cash, inflation)
    daily.to_csv(out / "daily_active_risk.csv", index_label="date")
    last = len(decisions) - 1
    score = (prices.shift(21) / prices.shift(126) - 1.0).where(members & prices.notna())
    vol = prices.pct_change(fill_method=None).rolling(20, min_periods=20).std()
    why = explain_positions(decisions[last], {s: float(v) for s, v in score.iloc[last].dropna().items()},
                            {s: float(v) for s, v in vol.iloc[last].dropna().items()})
    header = f"# Neden bu pozisyon ({prices.index[last].date()} kararı)"
    (out / "why_positions.md").write_text("\n\n".join([header, f"> {NOTICE_TR}", why]) + "\n", encoding="utf-8")
    note = latest_evidence_note(Path(args.evidence_report) if args.evidence_report else None)
    (out / "weekly_summary.md").write_text(weekly_summary(daily, inflation, note, interest_earned=ledger.interest_earned), encoding="utf-8")
    print(f"Reports written to {out}: decision_journal.jsonl, daily_active_risk.csv, why_positions.md, weekly_summary.md")
    print(NOTICE_TR)


NOTICE_TR = "Yerel simüle ledger; emir/broker yok. Araştırma çıktısıdır, yatırım tavsiyesi değildir."


def cmd_decision_package(args) -> None:
    """Dated report package folder (markdown + CSV): hypothesis summary, why-trace, active-risk CSV, real returns, cash interest."""
    from usa_signal_bot.decision.package import build_package
    from usa_signal_bot.evidence.cli import _cash_rate, _inflation

    data = load_csv_market(args.csv_dir, args.memberships) if args.source == "csv" else synthetic_market(seed=args.seed)
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(data.prices.index, data.prices.columns)
    out = build_package(data.prices, members, Path(args.out_dir), hypothesis_log=Path(args.hypothesis_log) if args.hypothesis_log else None,
                        evidence_report=Path(args.evidence_report) if args.evidence_report else None, cash_rate=_cash_rate(args),
                        inflation=_inflation(args, data), cash=args.cash, cost=CostModel(args.commission_bps, args.slippage_bps))
    print(f"Package written to {out}")
    print(NOTICE_TR)


def setup_decision_cli(subparsers) -> None:
    k = subparsers.add_parser("decision-package", help="Dated report package (markdown + CSV) from the simulated ledger and hypothesis log")
    k.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    k.add_argument("--csv-dir", default=None)
    k.add_argument("--memberships", default=None)
    k.add_argument("--seed", type=int, default=7)
    k.add_argument("--cash", type=float, default=100000.0)
    k.add_argument("--cash-rate", type=float, default=0.02)
    k.add_argument("--cash-rate-csv", default=None)
    k.add_argument("--inflation", type=float, default=0.025)
    k.add_argument("--inflation-csv", default=None)
    k.add_argument("--commission-bps", type=float, default=1.0)
    k.add_argument("--slippage-bps", type=float, default=5.0)
    k.add_argument("--hypothesis-log", default=None)
    k.add_argument("--evidence-report", default=None)
    k.add_argument("--out-dir", default="data/report_packages", help="package goes to <out-dir>/<date>/")
    k.set_defaults(func=cmd_decision_package)

    r = subparsers.add_parser("decision-report", help="Decision journal, why-position trace, daily active-risk CSV, weekly summary (simulated)")
    r.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    r.add_argument("--csv-dir", default=None)
    r.add_argument("--memberships", default=None)
    r.add_argument("--seed", type=int, default=7)
    r.add_argument("--cash", type=float, default=100000.0)
    r.add_argument("--cash-rate", type=float, default=0.02)
    r.add_argument("--cash-rate-csv", default=None)
    r.add_argument("--inflation", type=float, default=0.025)
    r.add_argument("--inflation-csv", default=None)
    r.add_argument("--commission-bps", type=float, default=1.0)
    r.add_argument("--slippage-bps", type=float, default=5.0)
    r.add_argument("--evidence-report", default=None, help="Evidence markdown whose **Sonuç:** line is quoted in the weekly summary")
    r.add_argument("--out-dir", default="data/reports")
    r.set_defaults(func=cmd_decision_report)

    p = subparsers.add_parser("decision-simulate", help="Run the decision pipeline on the local paper ledger (simulated)")
    p.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    p.add_argument("--csv-dir", default=None)
    p.add_argument("--memberships", default=None)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--cash", type=float, default=100000.0)
    p.add_argument("--cash-rate", type=float, default=0.02, help="Annual interest on idle cash (ASSUMPTION; default 2%%)")
    p.add_argument("--commission-bps", type=float, default=1.0)
    p.add_argument("--slippage-bps", type=float, default=5.0)
    p.add_argument("--journal", default=None, help="Optional JSONL path for simulated fills")
    p.set_defaults(func=cmd_decision_simulate)
