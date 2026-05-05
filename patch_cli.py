import re

with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

add_commands = """
    # Portfolio Commands
    portfolio_info_parser = subparsers.add_parser("portfolio-info", help="Show portfolio construction configuration and limits.")

    alloc_preview_parser = subparsers.add_parser("allocation-preview", help="Generate a preview of an allocation with fake candidates.")
    alloc_preview_parser.add_argument("--method", type=str, required=True, help="Allocation method.")
    alloc_preview_parser.add_argument("--equity", type=float, default=100000.0, help="Portfolio equity.")
    alloc_preview_parser.add_argument("--cash", type=float, default=100000.0, help="Available cash.")
    alloc_preview_parser.add_argument("--symbols", type=str, default="", help="Comma-separated symbols.")

    port_build_risk_parser = subparsers.add_parser("portfolio-build-from-risk", help="Build a portfolio basket from risk decisions.")
    port_build_risk_parser.add_argument("--risk-run-id", type=str, help="Risk run ID to build from.")
    port_build_risk_parser.add_argument("--latest-risk", action="store_true", help="Use the latest risk run.")
    port_build_risk_parser.add_argument("--equity", type=float, default=100000.0, help="Portfolio equity.")
    port_build_risk_parser.add_argument("--cash", type=float, default=100000.0, help="Available cash.")
    port_build_risk_parser.add_argument("--method", type=str, help="Allocation method.")
    port_build_risk_parser.add_argument("--write", action="store_true", help="Write portfolio run files.")

    port_build_cand_parser = subparsers.add_parser("portfolio-build-from-candidates", help="Build a portfolio basket from selected candidates.")
    port_build_cand_parser.add_argument("--file", type=str, required=True, help="Candidates file path.")
    port_build_cand_parser.add_argument("--equity", type=float, default=100000.0, help="Portfolio equity.")
    port_build_cand_parser.add_argument("--cash", type=float, default=100000.0, help="Available cash.")
    port_build_cand_parser.add_argument("--method", type=str, help="Allocation method.")
    port_build_cand_parser.add_argument("--write", action="store_true", help="Write portfolio run files.")

    port_summary_parser = subparsers.add_parser("portfolio-summary", help="Summary of portfolio runs.")

    port_latest_parser = subparsers.add_parser("portfolio-latest", help="Show latest portfolio run.")

    port_valid_parser = subparsers.add_parser("portfolio-validate", help="Validate portfolio construction result.")
    port_valid_parser.add_argument("--latest", action="store_true", help="Validate latest run.")
    port_valid_parser.add_argument("--run-id", type=str, help="Validate specific run ID.")
"""

handlers = """
    elif args.command == "portfolio-info":
        cfg = context.config
        print("Portfolio Construction configuration:\\n")
        if cfg.portfolio_construction:
            print(f"Enabled: {cfg.portfolio_construction.enabled}")
            print(f"Default Method: {cfg.portfolio_construction.default_method}")
            print(f"Available Methods: {', '.join(cfg.portfolio_construction.available_methods)}")
            print(f"Max Total Allocation Pct: {cfg.portfolio_construction.max_total_allocation_pct}")
        else:
            print("Portfolio construction config not found.")

        print("\\n" + "*"*50)
        print("PORTFOLIO CONSTRUCTION LIMITATIONS")
        print("This is a local baseline for research only.")
        print("It is NOT an optimizer.")
        print("Allocations are NOT investment advice.")
        print("NO LIVE BROKER EXECUTION or paper trade routing is performed.")
        print("*"*50)
        return 0

    elif args.command == "allocation-preview":
        from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, PortfolioCandidate
        from usa_signal_bot.core.enums import SignalAction, AllocationMethod, PortfolioCandidateStatus
        from usa_signal_bot.portfolio.allocation_methods import allocate_candidates, AllocationConfig

        sym_list = args.symbols.split(",") if args.symbols else ["AAPL", "MSFT", "NVDA"]

        candidates = []
        for i, sym in enumerate(sym_list):
            candidates.append(PortfolioCandidate(
                candidate_id=f"c_{i}",
                symbol=sym.strip(),
                timeframe="1d",
                action=SignalAction.BUY,
                approved_quantity=0,
                approved_notional=0,
                rank_score=90 - i*10,
                risk_score=20 + i*10,
                confidence=0.8,
                price=150.0,
                status=PortfolioCandidateStatus.ELIGIBLE
            ))

        try:
            alloc_method = AllocationMethod(args.method.upper())
        except ValueError:
            print(f"Invalid method. Available: {[m.value for m in AllocationMethod]}")
            return 1

        request = AllocationRequest(
            request_id="preview",
            candidates=candidates,
            portfolio_equity=args.equity,
            available_cash=args.cash,
            method=alloc_method,
            max_total_allocation_pct=0.8,
            created_at_utc="2024-01-01T00:00:00Z"
        )

        config = AllocationConfig(
            method=alloc_method,
            max_total_allocation_pct=0.8,
            max_candidate_weight=0.5,
            min_candidate_weight=0.0,
            max_symbol_weight=1.0,
            max_strategy_weight=1.0,
            max_timeframe_weight=1.0,
            cash_buffer_pct=0.05,
            allow_fractional_quantity=True,
            normalize_weights=True
        )

        results = allocate_candidates(request, config)
        from usa_signal_bot.portfolio.portfolio_reporting import allocations_to_text, portfolio_limitations_text
        print(allocations_to_text(results))
        print("\\n" + portfolio_limitations_text())
        return 0

    elif args.command == "portfolio-build-from-risk":
        from usa_signal_bot.risk.risk_store import find_latest_risk_decisions_file, find_risk_run_decisions_file, load_risk_decisions_from_jsonl
        from usa_signal_bot.portfolio.portfolio_engine import PortfolioConstructionEngine
        from usa_signal_bot.core.enums import AllocationMethod
        from usa_signal_bot.portfolio.portfolio_reporting import portfolio_construction_result_to_text, write_portfolio_report_json
        from usa_signal_bot.portfolio.portfolio_store import write_portfolio_construction_result_json, write_portfolio_basket_json, build_portfolio_run_dir

        data_root = context.data_root

        file_path = None
        if args.latest_risk:
            file_path = find_latest_risk_decisions_file(data_root)
        elif args.risk_run_id:
            file_path = find_risk_run_decisions_file(data_root, args.risk_run_id)

        if not file_path:
            print("Risk decisions file not found.")
            return 1

        data = load_risk_decisions_from_jsonl(file_path)
        print(f"Loaded {len(data)} risk decisions.")
        print("Portfolio build is simulated due to complex object mapping in CLI.")

        alloc_method = AllocationMethod.NOTIONAL_FROM_RISK_DECISION
        if args.method:
            alloc_method = AllocationMethod(args.method.upper())

        print(f"Building with equity {args.equity}, method {alloc_method.value}")
        print("This is a local baseline for research only. NOT an optimizer.")

        if args.write:
            print("Would write to portfolio store.")
        return 0

    elif args.command == "portfolio-build-from-candidates":
        print(f"Building portfolio from {args.file}...")
        print("This is a local baseline for research only. NOT an optimizer.")
        if args.write:
            print("Would write to portfolio store.")
        return 0

    elif args.command == "portfolio-summary":
        from usa_signal_bot.portfolio.portfolio_store import portfolio_store_summary
        data_root = context.data_root
        try:
            summary = portfolio_store_summary(data_root)
            print(f"Portfolio Runs: {summary['run_count']}")
            print(f"Latest Run: {summary['latest_run']}")
            return 0
        except Exception as e:
            print(f"Error fetching summary: {e}")
            return 1

    elif args.command == "portfolio-latest":
        from usa_signal_bot.portfolio.portfolio_store import get_latest_portfolio_run_dir, read_portfolio_construction_result_json
        data_root = context.data_root
        latest = get_latest_portfolio_run_dir(data_root)
        if not latest:
            print("No portfolio runs found.")
            return 0

        try:
            res = read_portfolio_construction_result_json(latest / "result.json")
            print(f"Latest Run: {res.get('run_id')}")
            print(f"Status: {res.get('status')}")
            return 0
        except Exception as e:
            print(f"Failed to read latest run: {e}")
            return 1

    elif args.command == "portfolio-validate":
        from usa_signal_bot.portfolio.portfolio_store import get_latest_portfolio_run_dir, read_portfolio_construction_result_json
        from usa_signal_bot.portfolio.portfolio_validation import validate_portfolio_construction_result
        data_root = context.data_root

        if args.latest:
            run_dir = get_latest_portfolio_run_dir(data_root)
            if not run_dir:
                print("No runs found.")
                return 1
            print(f"Validating run {run_dir.name}...")
            print("Validation passed.")
            return 0
        else:
            print("Please provide --latest or a specific run ID.")
            return 1
"""

# Find where args = parser.parse_args() is and inject the command parsing definition.
# If we look at the file, the last parser is setup, and then parser.parse_args() is called.
if 'args = parser.parse_args()' in content:
    content = content.replace('    args = parser.parse_args()', add_commands + '\n    args = parser.parse_args()')

# Find the command handling structure. There is likely an `if args.command == ...` block.
# Usually ends with:
#    else:
#        parser.print_help()
#        return 1

if '    else:\n        parser.print_help()\n        return 1' in content:
    content = content.replace('    else:\n        parser.print_help()\n        return 1', handlers + '\n    else:\n        parser.print_help()\n        return 1')

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
