"""CLI: ``python -m usa_signal_bot evidence-run`` (research only, writes a markdown report)."""

from __future__ import annotations

from pathlib import Path

from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.evidence.data import load_csv_market, synthetic_market
from usa_signal_bot.evidence.report import run_evidence


def _cash_rate(args):
    if getattr(args, "cash_rate_csv", None):
        from usa_signal_bot.evidence.rates import load_rate_csv

        return load_rate_csv(args.cash_rate_csv)
    return args.cash_rate


def _inflation(args, data):
    """Annual inflation: realised CPI (--inflation-csv, index level) over the data span, else the --inflation assumption."""
    if getattr(args, "inflation_csv", None):
        from usa_signal_bot.evidence.rates import average_inflation, load_rate_csv

        level = load_rate_csv(args.inflation_csv, percent=False)
        idx = data.prices.index
        return average_inflation(level, idx[0], idx[-1])
    return args.inflation


def _fundamentals(args):
    if not getattr(args, "fundamentals_dir", None):
        return None
    from usa_signal_bot.evidence.fundamentals import load_fundamentals

    return load_fundamentals(args.fundamentals_dir)


def _macro(args):
    if not getattr(args, "macro_dir", None):
        return None
    from usa_signal_bot.evidence.macro_regime import fetch_macro, load_macro

    if getattr(args, "fetch_macro", False):
        print("macro fetch:", fetch_macro(args.macro_dir))
    return load_macro(args.macro_dir) or None


def _etf(args):
    if not getattr(args, "etf_dir", None):
        return None
    from usa_signal_bot.evidence.sector_rotation import fetch_etf_prices, load_etf_prices

    if getattr(args, "fetch_etf", False):
        res = fetch_etf_prices(args.etf_dir)
        print(f"etf fetch ok={len(res['ok'])} failed={res['failed']}")
    df = load_etf_prices(args.etf_dir)
    return None if df.empty else df


def _hlog(args):
    if not getattr(args, "hypothesis_log", None):
        return None
    from usa_signal_bot.evidence.hypothesis_log import HypothesisLog
    from datetime import datetime, timezone

    return HypothesisLog(Path(args.hypothesis_log), clock=lambda: datetime.now(timezone.utc).isoformat())


def cmd_evidence_run(args) -> None:
    if args.source == "csv":
        if not args.csv_dir:
            raise SystemExit("--csv-dir is required with --source csv")
        data = load_csv_market(args.csv_dir, args.memberships)
    else:
        data = synthetic_market(seed=args.seed)
    report = run_evidence(data, CostModel(args.commission_bps, args.slippage_bps), seed=args.seed,
                          families=args.families.split(",") if args.families else None,
                          hypothesis_log=_hlog(args), run_id=f"run-seed{args.seed}",
                          cash_rate=_cash_rate(args), fundamentals=_fundamentals(args), macro=_macro(args), etf_prices=_etf(args), inflation=_inflation(args, data))
    text = report.to_markdown()
    print(text)
    if args.write:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Written to {out}")


def cmd_evidence_fetch(args) -> None:
    """Download prices (yfinance) and EDGAR fundamentals for the universe. EDGAR needs SEC_USER_AGENT in the environment."""
    from usa_signal_bot.evidence.edgar import EdgarClient
    from usa_signal_bot.evidence.fetch import DEFAULT_TICKERS, fetch_daily
    from usa_signal_bot.evidence.fundamentals import fetch_fundamentals

    client = EdgarClient(args.edgar_cache)
    if args.universe == "sec-top":
        tickers = client.top_registrants(args.n)
    else:
        tickers = list(DEFAULT_TICKERS)
    if args.prices:
        res = fetch_daily(tickers, args.csv_dir, start=args.start)
        print(f"prices ok={len(res['ok'])} failed={len(res['failed'])} splits={res['splits']}")
        tickers = res["ok"]
    if args.fundamentals_dir:
        st = fetch_fundamentals(client, tickers, args.fundamentals_dir)
        from collections import Counter

        print("fundamentals:", dict(Counter(v.split(":")[0] for v in st.values())))


def setup_evidence_cli(subparsers) -> None:
    f = subparsers.add_parser("evidence-fetch", help="Download prices (yfinance) and EDGAR fundamentals (research data only)")
    f.add_argument("--universe", choices=["default50", "sec-top"], default="default50")
    f.add_argument("--n", type=int, default=300, help="size for --universe sec-top")
    f.add_argument("--csv-dir", default="data/prices")
    f.add_argument("--start", default="2010-01-01")
    f.add_argument("--prices", action="store_true", help="download prices")
    f.add_argument("--fundamentals-dir", default=None, help="download compact EDGAR facts here")
    f.add_argument("--edgar-cache", default="data/edgar_cache")
    f.set_defaults(func=cmd_evidence_fetch)

    p = subparsers.add_parser("evidence-run", help="Walk-forward strategy evidence report (research only)")
    p.add_argument("--source", choices=["synthetic", "csv"], default="synthetic")
    p.add_argument("--csv-dir", default=None, help="Directory with <SYMBOL>.csv price files")
    p.add_argument("--memberships", default=None, help="CSV with symbol,start,end (point-in-time universe)")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--commission-bps", type=float, default=1.0)
    p.add_argument("--slippage-bps", type=float, default=5.0)
    p.add_argument("--families", default=None, help="Comma-separated strategy family names (default: all)")
    p.add_argument("--hypothesis-log", default=None, help="JSONL file recording every evaluated candidate (cumulative trial count for DSR)")
    p.add_argument("--cash-rate", type=float, default=0.02, help="Annual interest on idle cash (ASSUMPTION; default 2%%)")
    p.add_argument("--cash-rate-csv", default=None, help="FRED-style CSV (e.g. DTB3) for a historical cash rate; overrides --cash-rate")
    p.add_argument("--inflation", type=float, default=0.025, help="Annual inflation assumption for real CAGR (default 2.5%%)")
    p.add_argument("--inflation-csv", default=None, help="FRED CPIAUCSL-style CSV (index level); realised inflation over the data span overrides --inflation")
    p.add_argument("--fundamentals-dir", default=None, help="Compact EDGAR facts (evidence-fetch); adds true value/quality families")
    p.add_argument("--macro-dir", default=None, help="Dir with FRED CSVs (T10Y2Y, VIXCLS, BAA10Y); adds the macro regime family")
    p.add_argument("--fetch-macro", action="store_true", help="download/refresh the FRED CSVs into --macro-dir (public CSV endpoint)")
    p.add_argument("--etf-dir", default=None, help="Dir with sector ETF + SPY CSVs; adds the sector rotation families")
    p.add_argument("--fetch-etf", action="store_true", help="download/refresh sector ETFs + SPY (yfinance) into --etf-dir")
    p.add_argument("--write", action="store_true")
    p.add_argument("--out", default="data/evidence/evidence_report.md")
    p.set_defaults(func=cmd_evidence_run)
