import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch, load_strategy_feature_frames_from_feature_store, filter_valid_strategy_frames
from usa_signal_bot.strategies.strategy_models import StrategyRunResult, create_strategy_run_id
from usa_signal_bot.strategies.signal_validation import validate_signal_list, assert_signals_valid
from usa_signal_bot.strategies.signal_store import write_signals_jsonl, write_signal_validation_report_json, build_signal_output_path
from usa_signal_bot.core.enums import StrategyRunStatus
from usa_signal_bot.core.exceptions import StrategyExecutionError

class StrategyEngine:
    def __init__(self, registry: StrategyRegistry, data_root: Path):
        self.registry = registry
        self.data_root = data_root

    def run_strategy(self, strategy_name: str, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None, write_outputs: bool = False) -> StrategyRunResult:
        run_id = create_strategy_run_id(strategy_name)
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        try:
            strategy = self.registry.get(strategy_name)

            # Input validation
            val_results = strategy.validate_input(batch)
            valid_batch = filter_valid_strategy_frames(batch, val_results)

            warnings = []
            errors = []

            invalid_count = sum(1 for r in val_results if not r.valid)
            if invalid_count > 0:
                warnings.append(f"{invalid_count} frames failed input validation.")

            # Generate signals
            signals = strategy.generate_signals(valid_batch, params)

            # Validate output
            val_report = validate_signal_list(signals)

            # Add validation warnings/errors
            warnings.extend(val_report.warnings)
            errors.extend(val_report.errors)

            status = StrategyRunStatus.COMPLETED
            if val_report.invalid_signals > 0:
                status = StrategyRunStatus.PARTIAL_SUCCESS

            if not signals:
                warnings.append("Strategy generated 0 signals.")

            # Ensure proper signal IDs and strategy names
            for s in signals:
                if not hasattr(s, "signal_id") or not s.signal_id:
                    from usa_signal_bot.strategies.signal_contract import create_signal_id
                    s.signal_id = create_signal_id(strategy_name, s.symbol, s.timeframe, s.timestamp_utc)
                s.strategy_name = strategy_name

            result = StrategyRunResult(
                run_id=run_id,
                strategy_name=strategy_name,
                status=status,
                signals=signals,
                symbols_processed=list(set(f.symbol for f in valid_batch.frames)),
                timeframes_processed=list(set(f.timeframe for f in valid_batch.frames)),
                warnings=warnings,
                errors=errors,
                created_at_utc=now_utc
            )

            if write_outputs:
                self.write_strategy_result(result, val_report)

            return result

        except Exception as e:
            return StrategyRunResult(
                run_id=run_id,
                strategy_name=strategy_name,
                status=StrategyRunStatus.FAILED,
                signals=[],
                symbols_processed=[],
                timeframes_processed=[],
                warnings=[],
                errors=[str(e)],
                created_at_utc=now_utc
            )

    def run_strategies(self, strategy_names: List[str], batch: StrategyInputBatch, params_by_strategy: Optional[Dict[str, Dict[str, Any]]] = None, write_outputs: bool = False) -> List[StrategyRunResult]:
        results = []
        params_by_strategy = params_by_strategy or {}

        for name in strategy_names:
            params = params_by_strategy.get(name)
            res = self.run_strategy(name, batch, params, write_outputs)
            results.append(res)

        return results

    def run_strategy_from_feature_store(self, strategy_name: str, symbols: List[str], timeframes: List[str], params: Optional[Dict[str, Any]] = None, write_outputs: bool = False) -> StrategyRunResult:
        try:
            strategy = self.registry.get(strategy_name)
            feature_names = strategy.metadata.required_features + strategy.metadata.optional_features

            batch = load_strategy_feature_frames_from_feature_store(self.data_root, symbols, timeframes, feature_names)
            return self.run_strategy(strategy_name, batch, params, write_outputs)
        except Exception as e:
            run_id = create_strategy_run_id(strategy_name)
            now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
            return StrategyRunResult(
                run_id=run_id,
                strategy_name=strategy_name,
                status=StrategyRunStatus.FAILED,
                signals=[],
                symbols_processed=symbols,
                timeframes_processed=timeframes,
                warnings=[],
                errors=[str(e)],
                created_at_utc=now_utc
            )

    def write_strategy_result(self, result: StrategyRunResult, validation_report: Any = None) -> List[Path]:
        paths = []
        if not result.signals:
            return paths

        # Group signals by timeframe for storage
        tf_signals = {}
        for s in result.signals:
            if s.timeframe not in tf_signals:
                tf_signals[s.timeframe] = []
            tf_signals[s.timeframe].append(s)

        for tf, signals in tf_signals.items():
            path = build_signal_output_path(self.data_root, result.strategy_name, tf, result.run_id, "jsonl")
            write_signals_jsonl(path, signals)
            paths.append(path)

            if validation_report:
                report_path = path.with_suffix(".val.json")
                write_signal_validation_report_json(report_path, validation_report)
                paths.append(report_path)

        return paths
