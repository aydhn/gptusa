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


def setup_decision_cli(subparsers) -> None:
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
