import re

with open("usa_signal_bot/app/cli.py", "r") as f:
    content = f.read()

functions_code = """
def command_robustness_info(args) -> int:
    try:
        from usa_signal_bot.core.config import load_app_config
        config = load_app_config()
        mc = getattr(config, 'monte_carlo', None)
        bt = getattr(config, 'bootstrap_analysis', None)
        st = getattr(config, 'stress_testing', None)
        rb = getattr(config, 'robustness', None)

        print("Robustness & Stress Testing Configuration")
        print("-" * 80)

        if mc:
            print("Monte Carlo Simulation:")
            print(f"  Enabled: {mc.enabled}")
            print(f"  Default Type: {mc.default_simulation_type}")
            print(f"  Iterations: {mc.default_iterations} (Max: {mc.max_iterations})")
            print(f"  Random Seed: {mc.random_seed}")

        if bt:
            print("\\nBootstrap Analysis:")
            print(f"  Enabled: {bt.enabled}")
            print(f"  Default Percentiles: {bt.default_percentiles}")

        if st:
            print("\\nStress Testing:")
            print(f"  Enabled: {st.enabled}")
            print(f"  Missing Trade Fraction: {st.missing_trade_fraction}")
            print(f"  Fee/Slippage Multipliers: {st.fee_stress_multiplier}x / {st.slippage_stress_multiplier}x")

        if rb:
             print("\\nRobustness Score:")
             print(f"  Enabled: {rb.enabled}")
             print(f"  Thresholds: VR > {rb.very_robust_score} | R > {rb.robust_score} | M > {rb.moderate_score} | F > {rb.fragile_score}")

        print("\\n" + "="*80)
        print("IMPORTANT LIMITATION: Robustness scores and Monte Carlo percentile bands")
        print("are based on historical distributions and DO NOT guarantee future performance.")
        print("="*80)

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def _load_ledger_and_curve(run_dir):
    import json
    from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade, TradeDirection, TradeStatus
    from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint
    from usa_signal_bot.core.enums import TradeDirection as ETradeDirection

    ledger = None
    curve = None

    ledger_path = run_dir / "trade_ledger.json"
    if ledger_path.exists():
        with open(ledger_path, "r") as f:
            l_data = json.load(f)
            trades = []
            for t in l_data.get("closed_trades", []):
                trades.append(BacktestTrade(
                    trade_id=t.get("trade_id", "unknown"),
                    symbol=t.get("symbol", "unknown"),
                    timeframe=t.get("timeframe", "1d"),
                    direction=ETradeDirection(t.get("direction", "LONG")),
                    status=TradeStatus.CLOSED,
                    entry_fill_id=None, exit_fill_id=None,
                    entry_time_utc=t.get("entry_time_utc", ""),
                    exit_time_utc=t.get("exit_time_utc", ""),
                    entry_price=t.get("entry_price", 0.0),
                    exit_price=t.get("exit_price", 0.0),
                    quantity=t.get("quantity", 0.0),
                    gross_pnl=t.get("gross_pnl", 0.0),
                    net_pnl=t.get("net_pnl", 0.0),
                    total_fees=t.get("total_fees", 0.0),
                    total_slippage_cost=t.get("total_slippage_cost", 0.0),
                    return_pct=t.get("return_pct", 0.0),
                    holding_bars=None, holding_seconds=None,
                    exit_reason=t.get("exit_reason", "UNKNOWN"),
                    signal_id=None, strategy_name=None
                ))
            ledger = TradeLedger(ledger_id=l_data.get("ledger_id", "simulated"), trades=trades, open_trades=[], closed_trades=trades, created_at_utc="")

    curve_path = run_dir / "equity_curve.json"
    if curve_path.exists():
        with open(curve_path, "r") as f:
            c_data = json.load(f)
            points = []
            for p in c_data.get("points", []):
                 points.append(EquityCurvePoint(
                      timestamp_utc=p.get("timestamp_utc", ""),
                      equity=p.get("equity", 0.0),
                      cash=p.get("cash", 0.0),
                      realized_pnl=0.0, unrealized_pnl=0.0, drawdown=0.0, drawdown_pct=0.0
                 ))
            curve = EquityCurve(points=points, starting_cash=c_data.get("starting_cash", 100000.0), ending_equity=c_data.get("ending_equity"), max_drawdown=None, max_drawdown_pct=None)

    return ledger, curve

def command_monte_carlo_run(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.core.config import load_app_config
        from usa_signal_bot.backtesting.backtest_store import find_latest_backtest_run_dir, find_backtest_run_dir
        from usa_signal_bot.backtesting.monte_carlo_models import MonteCarloConfig
        from usa_signal_bot.core.enums import MonteCarloSimulationType
        from usa_signal_bot.backtesting.monte_carlo_simulator import MonteCarloSimulator
        from usa_signal_bot.backtesting.robustness_store import build_robustness_run_dir, write_monte_carlo_result_json, write_monte_carlo_paths_jsonl
        from usa_signal_bot.backtesting.robustness_reporting import monte_carlo_result_to_text, write_robustness_report_json

        config = load_app_config()
        mc_config_base = getattr(config, 'monte_carlo', None)

        data_root = Path("data")
        run_dir = None
        if args.run_id:
            run_dir = find_backtest_run_dir(data_root, args.run_id)
        elif getattr(args, "latest_backtest", False):
            run_dir = find_latest_backtest_run_dir(data_root)

        if not run_dir:
            print("Error: Backtest run not found.")
            return 1

        ledger, curve = _load_ledger_and_curve(run_dir)
        if not ledger and not curve:
            print("Error: Trade ledger and equity curve missing from backtest run.")
            return 1

        sim_type = MonteCarloSimulationType(args.type) if getattr(args, "type", None) else MonteCarloSimulationType(mc_config_base.default_simulation_type if mc_config_base else "TRADE_BOOTSTRAP")
        iterations = getattr(args, "iterations", None) or (mc_config_base.default_iterations if mc_config_base else 1000)
        seed = getattr(args, "seed", None) or (mc_config_base.random_seed if mc_config_base else 42)

        mc_conf = MonteCarloConfig(
            simulation_type=sim_type,
            iterations=iterations,
            starting_cash=curve.starting_cash if curve else 100000.0,
            random_seed=seed,
            max_iterations=mc_config_base.max_iterations if mc_config_base else 10000
        )

        simulator = MonteCarloSimulator(random_seed=seed)

        if sim_type == MonteCarloSimulationType.TRADE_BOOTSTRAP:
             if not ledger:
                  print("Error: Trade ledger required for trade bootstrap.")
                  return 1
             res = simulator.run_trade_bootstrap(ledger, mc_conf, run_dir.name)
        elif sim_type == MonteCarloSimulationType.EQUITY_RETURN_BOOTSTRAP:
             if not curve:
                  print("Error: Equity curve required for equity bootstrap.")
                  return 1
             res = simulator.run_equity_return_bootstrap(curve, mc_conf, run_dir.name)
        elif sim_type == MonteCarloSimulationType.TRADE_ORDER_PERMUTATION:
             if not ledger:
                  print("Error: Trade ledger required for permutation.")
                  return 1
             res = simulator.run_trade_order_permutation(ledger, mc_conf, run_dir.name)
        else:
             print(f"Error: Unsupported simulation type: {sim_type}")
             return 1

        print(monte_carlo_result_to_text(res))

        if getattr(args, "write", False):
            rd = build_robustness_run_dir(data_root, res.run_id)
            write_monte_carlo_result_json(rd / "monte_carlo_result.json", res)
            if res.paths:
                 write_monte_carlo_paths_jsonl(rd / "paths.jsonl", res.paths)
            write_robustness_report_json(rd / "report.json", res)
            print(f"\\nResults written to: {rd}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_bootstrap_run(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.backtest_store import find_latest_backtest_run_dir, find_backtest_run_dir
        from usa_signal_bot.backtesting.bootstrap_analysis import (
             extract_trade_net_returns, extract_equity_returns,
             bootstrap_trade_returns, bootstrap_equity_returns, percentile_summary
        )

        data_root = Path("data")
        run_dir = None
        if args.run_id:
            run_dir = find_backtest_run_dir(data_root, args.run_id)
        elif getattr(args, "latest_backtest", False):
            run_dir = find_latest_backtest_run_dir(data_root)

        if not run_dir:
            print("Error: Backtest run not found.")
            return 1

        ledger, curve = _load_ledger_and_curve(run_dir)
        source = getattr(args, "source", "trades")
        iterations = getattr(args, "iterations", 1000)
        if not iterations: iterations = 1000

        print(f"Running Bootstrap Analysis (Source: {source}, Iterations: {iterations})")
        print("-" * 80)

        if source == "trades":
             if not ledger:
                  print("Error: Ledger not found.")
                  return 1
             rets = extract_trade_net_returns(ledger)
             samples = bootstrap_trade_returns(rets, iterations)
        else:
             if not curve:
                  print("Error: Equity curve not found.")
                  return 1
             rets = extract_equity_returns(curve)
             samples = bootstrap_equity_returns(rets, iterations)

        total_rets = []
        for s in samples:
             r = sum(s)
             total_rets.append(r)

        p_sum = percentile_summary(total_rets)
        for k, v in p_sum.items():
             print(f"  {k}: {(v or 0)*100:.2f}%")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_stress_test_run(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.backtest_store import find_latest_backtest_run_dir, find_backtest_run_dir
        from usa_signal_bot.backtesting.stress_scenarios import (
             run_stress_scenario_set, default_stress_scenarios,
             build_fee_slippage_stress_scenario, build_missing_winners_scenario,
             build_missing_random_trades_scenario, build_worst_sequence_scenario
        )
        from usa_signal_bot.backtesting.robustness_reporting import stress_scenario_results_to_text
        from usa_signal_bot.backtesting.robustness_store import build_robustness_run_dir, write_stress_scenario_results_json
        import uuid

        data_root = Path("data")
        run_dir = None
        if args.run_id:
            run_dir = find_backtest_run_dir(data_root, args.run_id)
        elif getattr(args, "latest_backtest", False):
            run_dir = find_latest_backtest_run_dir(data_root)

        if not run_dir:
            print("Error: Backtest run not found.")
            return 1

        ledger, _ = _load_ledger_and_curve(run_dir)
        if not ledger:
             print("Error: Trade ledger required for stress scenarios.")
             return 1

        scenario = getattr(args, "scenario", "default")
        configs = []
        if scenario == "default":
             configs = default_stress_scenarios()
        elif scenario == "missing_winners":
             configs = [build_missing_winners_scenario()]
        elif scenario == "missing_random_trades":
             configs = [build_missing_random_trades_scenario()]
        elif scenario == "worst_sequence":
             configs = [build_worst_sequence_scenario()]
        elif scenario == "cost_slippage":
             configs = [build_fee_slippage_stress_scenario()]
        else:
             print("Unknown scenario")
             return 1

        results = run_stress_scenario_set(ledger, configs)
        print(stress_scenario_results_to_text(results))

        if getattr(args, "write", False):
             rd = build_robustness_run_dir(data_root, f"stress_{str(uuid.uuid4())[:8]}")
             write_stress_scenario_results_json(rd / "stress_scenarios.json", results)
             print(f"\\nResults written to: {rd}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_robustness_summary(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.robustness_store import list_robustness_runs
        import json

        data_root = Path("data")
        runs = list_robustness_runs(data_root)

        print("Robustness Runs Summary")
        print("-" * 80)
        if not runs:
            print("No robustness runs found.")
            return 0

        for r_dir in runs[:20]:
            mc_path = r_dir / "monte_carlo_result.json"
            if mc_path.exists():
                with open(mc_path, "r") as f:
                    data = json.load(f)
                rid = data.get("run_id", r_dir.name)
                st = data.get("status", "UNKNOWN")
                it = data.get("config", {}).get("iterations", 0)
                bucket = data.get("robustness_bucket", "UNKNOWN")
                print(f"ID: {rid} | Status: {st} | Iterations: {it} | Bucket: {bucket}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_robustness_latest(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.robustness_store import get_latest_robustness_run_dir
        import json

        data_root = Path("data")
        r_dir = get_latest_robustness_run_dir(data_root)

        if not r_dir:
            print("No robustness runs found.")
            return 0

        rep_path = r_dir / "report.json"
        if rep_path.exists():
             with open(rep_path, "r") as f:
                  data = json.load(f)
                  print(data.get("report_text", "Empty report"))
        else:
             print(f"Found latest run at {r_dir.name} but no report.json exists.")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_robustness_validate(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.robustness_store import get_latest_robustness_run_dir, build_robustness_run_dir

        data_root = Path("data")
        r_dir = None
        if args.run_id:
             r_dir = build_robustness_run_dir(data_root, args.run_id)
        elif getattr(args, "latest", False):
             r_dir = get_latest_robustness_run_dir(data_root)

        if not r_dir or not r_dir.exists():
             print("Validation FAILED: Run not found.")
             return 1

        has_mc = (r_dir / "monte_carlo_result.json").exists()
        has_paths = (r_dir / "paths.jsonl").exists()
        has_stress = (r_dir / "stress_scenarios.json").exists()

        print(f"Validating run: {r_dir.name}")
        print(f"  monte_carlo_result.json: {'OK' if has_mc else 'MISSING'}")
        print(f"  paths.jsonl:             {'OK' if has_paths else 'MISSING'}")
        print(f"  stress_scenarios.json:   {'OK' if has_stress else 'MISSING'}")

        if not has_mc and not has_stress:
             print("Validation FAILED: No robustness data found.")
             return 1

        print("Validation PASSED: Essential robustness files exist.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

"""
main_match = re.search(r'def main\(\) -> int:', content)
if main_match:
    content = content[:main_match.start()] + functions_code + "\n" + content[main_match.start():]

parser_add = """    p_rob_info = subparsers.add_parser("robustness-info", help="Show robustness configuration")

    p_mc = subparsers.add_parser("monte-carlo-run", help="Run Monte Carlo simulation")
    p_mc.add_argument("--run-id", type=str, help="Source backtest run id")
    p_mc.add_argument("--latest-backtest", action="store_true", help="Use latest backtest")
    p_mc.add_argument("--type", type=str, help="Simulation type (trade_bootstrap, equity_return_bootstrap, etc)")
    p_mc.add_argument("--iterations", type=int, help="Number of iterations")
    p_mc.add_argument("--seed", type=int, help="Random seed")
    p_mc.add_argument("--write", action="store_true", help="Write results to disk")

    p_boot = subparsers.add_parser("bootstrap-run", help="Run basic bootstrap analysis")
    p_boot.add_argument("--run-id", type=str, help="Source backtest run id")
    p_boot.add_argument("--latest-backtest", action="store_true", help="Use latest backtest")
    p_boot.add_argument("--source", type=str, default="trades", help="Source: trades or equity")
    p_boot.add_argument("--iterations", type=int, help="Number of iterations")
    p_boot.add_argument("--write", action="store_true", help="Write results to disk")

    p_stress = subparsers.add_parser("stress-test-run", help="Run stress scenarios")
    p_stress.add_argument("--run-id", type=str, help="Source backtest run id")
    p_stress.add_argument("--latest-backtest", action="store_true", help="Use latest backtest")
    p_stress.add_argument("--scenario", type=str, default="default", help="Scenario name")
    p_stress.add_argument("--write", action="store_true", help="Write results to disk")

    p_rob_sum = subparsers.add_parser("robustness-summary", help="Show robustness runs summary")
    p_rob_lat = subparsers.add_parser("robustness-latest", help="Show latest robustness run")
    p_rob_val = subparsers.add_parser("robustness-validate", help="Validate robustness run")
    p_rob_val.add_argument("--run-id", type=str, help="Run ID to validate")
    p_rob_val.add_argument("--latest", action="store_true", help="Validate latest run")

    args = parser.parse_args()"""

content = re.sub(r'    args = parser\.parse_args\(\)', parser_add, content)

main_add = """    elif args.command == "robustness-info":
        return command_robustness_info(args)
    elif args.command == "monte-carlo-run":
        return command_monte_carlo_run(args)
    elif args.command == "bootstrap-run":
        return command_bootstrap_run(args)
    elif args.command == "stress-test-run":
        return command_stress_test_run(args)
    elif args.command == "robustness-summary":
        return command_robustness_summary(args)
    elif args.command == "robustness-latest":
        return command_robustness_latest(args)
    elif args.command == "robustness-validate":
        return command_robustness_validate(args)
    else:"""
content = content.replace("    else:", main_add, 1)

with open("usa_signal_bot/app/cli.py", "w") as f:
    f.write(content)
