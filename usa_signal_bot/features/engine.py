from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timezone
import uuid
import pandas as pd

from usa_signal_bot.features.indicator_registry import IndicatorRegistry
from usa_signal_bot.features.input_contract import (
    FeatureInput, FeatureBatchInput, validate_feature_input,
    validate_feature_batch_input, build_feature_inputs_from_cache,
    filter_valid_feature_inputs
)
from usa_signal_bot.features.output_contract import (
    FeatureComputationRequest, FeatureComputationResult,
    FeatureRow, FeatureOutputMetadata
)
from usa_signal_bot.features.dataframe_utils import (
    bars_to_dataframe, dataframe_to_feature_rows,
    ensure_ohlcv_dataframe_columns, normalize_feature_dataframe
)
from usa_signal_bot.features.validation import validate_feature_rows
from usa_signal_bot.features.feature_store import (
    build_feature_output_path, write_feature_rows_jsonl,
    write_feature_rows_csv, write_feature_metadata_json, feature_store_dir
)
from usa_signal_bot.core.enums import FeatureComputationStatus, FeatureStorageFormat
from usa_signal_bot.core.exceptions import FeatureComputationError

class FeatureEngine:
    def __init__(self, registry: IndicatorRegistry, data_root: Path):
        self.registry = registry
        self.data_root = data_root

    def compute_for_input(self, input_: FeatureInput, indicator_names: List[str], params_by_indicator: Optional[Dict[str, Dict[str, Any]]] = None) -> FeatureComputationResult:
        params_by_indicator = params_by_indicator or {}

        req = FeatureComputationRequest(
            indicator_names=indicator_names,
            params_by_indicator=params_by_indicator,
            symbols=[input_.symbol],
            timeframes=[input_.timeframe],
            provider_name=input_.source
        )

        val_res = validate_feature_input(input_)
        if not val_res.valid:
            return FeatureComputationResult(
                request=req,
                status=FeatureComputationStatus.FAILED,
                feature_rows=[],
                produced_features=[],
                symbols_processed=[],
                timeframes_processed=[],
                warnings=[],
                errors=val_res.messages,
                created_at_utc=datetime.now(timezone.utc).isoformat()
            )

        try:
            df = bars_to_dataframe(input_.bars)
            ensure_ohlcv_dataframe_columns(df)

            produced_features = []
            errors = []
            warnings = []

            for name in indicator_names:
                try:
                    indicator = self.registry.get(name)
                    params = params_by_indicator.get(name, {})

                    ind_df = indicator.compute(df, params)

                    cols_to_add = [c for c in ind_df.columns if c not in df.columns]
                    if not cols_to_add:
                        warnings.append(f"Indicator {name} produced no new columns")
                    else:
                        for c in cols_to_add:
                            df[c] = ind_df[c]
                            produced_features.append(c)

                except Exception as e:
                    errors.append(f"Error computing indicator {name} for {input_.symbol}: {e}")

            df = normalize_feature_dataframe(df)

            feature_rows = dataframe_to_feature_rows(df, input_.symbol, input_.timeframe)

            status = FeatureComputationStatus.COMPLETED
            if errors and produced_features:
                status = FeatureComputationStatus.PARTIAL_SUCCESS
            elif errors and not produced_features:
                status = FeatureComputationStatus.FAILED

            return FeatureComputationResult(
                request=req,
                status=status,
                feature_rows=feature_rows,
                produced_features=produced_features,
                symbols_processed=[input_.symbol],
                timeframes_processed=[input_.timeframe],
                warnings=warnings,
                errors=errors,
                created_at_utc=datetime.now(timezone.utc).isoformat()
            )

        except Exception as e:
            return FeatureComputationResult(
                request=req,
                status=FeatureComputationStatus.FAILED,
                feature_rows=[],
                produced_features=[],
                symbols_processed=[],
                timeframes_processed=[],
                warnings=[],
                errors=[str(e)],
                created_at_utc=datetime.now(timezone.utc).isoformat()
            )

    def compute_for_batch(self, batch: FeatureBatchInput, indicator_names: List[str], params_by_indicator: Optional[Dict[str, Dict[str, Any]]] = None) -> FeatureComputationResult:
        params_by_indicator = params_by_indicator or {}

        all_symbols = list({inp.symbol for inp in batch.inputs})
        all_timeframes = list({inp.timeframe for inp in batch.inputs})

        req = FeatureComputationRequest(
            indicator_names=indicator_names,
            params_by_indicator=params_by_indicator,
            symbols=all_symbols,
            timeframes=all_timeframes,
            provider_name=batch.provider_name,
            universe_name=batch.universe_name
        )

        val_results = validate_feature_batch_input(batch)
        valid_batch = filter_valid_feature_inputs(batch, val_results)

        all_feature_rows = []
        all_produced_features = set()
        all_errors = []
        for v in val_results:
            if not v.valid:
                all_errors.extend(v.messages)

        all_warnings = []
        symbols_processed = set()
        timeframes_processed = set()

        for inp in valid_batch.inputs:
            res = self.compute_for_input(inp, indicator_names, params_by_indicator)
            all_feature_rows.extend(res.feature_rows)
            all_produced_features.update(res.produced_features)
            all_errors.extend(res.errors)
            all_warnings.extend(res.warnings)

            if res.is_successful():
                symbols_processed.add(inp.symbol)
                timeframes_processed.add(inp.timeframe)

        status = FeatureComputationStatus.COMPLETED
        if all_errors and all_feature_rows:
            status = FeatureComputationStatus.PARTIAL_SUCCESS
        elif all_errors and not all_feature_rows:
            status = FeatureComputationStatus.FAILED

        return FeatureComputationResult(
            request=req,
            status=status,
            feature_rows=all_feature_rows,
            produced_features=sorted(list(all_produced_features)),
            symbols_processed=sorted(list(symbols_processed)),
            timeframes_processed=sorted(list(timeframes_processed)),
            warnings=all_warnings,
            errors=all_errors,
            created_at_utc=datetime.now(timezone.utc).isoformat()
        )

    def compute_from_cache(self, symbols: List[str], timeframes: List[str], indicator_names: List[str], params_by_indicator: Optional[Dict[str, Dict[str, Any]]] = None, provider_name: str = "yfinance") -> FeatureComputationResult:
        batch = build_feature_inputs_from_cache(self.data_root, symbols, timeframes, provider_name)
        return self.compute_for_batch(batch, indicator_names, params_by_indicator)


    def compute_momentum_set_for_input(self, input_: FeatureInput, set_name: str = "basic_momentum") -> FeatureComputationResult:
        from usa_signal_bot.features.momentum_sets import get_momentum_indicator_set
        ind_set = get_momentum_indicator_set(set_name)
        return self.compute_for_input(input_, ind_set.indicators, ind_set.params_by_indicator)

    def compute_momentum_set_for_batch(self, batch: FeatureBatchInput, set_name: str = "basic_momentum") -> FeatureComputationResult:
        from usa_signal_bot.features.momentum_sets import get_momentum_indicator_set
        ind_set = get_momentum_indicator_set(set_name)
        return self.compute_for_batch(batch, ind_set.indicators, ind_set.params_by_indicator)

    def compute_momentum_set_from_cache(self, symbols: list[str], timeframes: list[str], set_name: str = "basic_momentum", provider_name: str = "yfinance") -> FeatureComputationResult:
        from usa_signal_bot.features.momentum_sets import get_momentum_indicator_set
        ind_set = get_momentum_indicator_set(set_name)
        return self.compute_from_cache(symbols, timeframes, ind_set.indicators, ind_set.params_by_indicator, provider_name)
    def compute_volatility_set_for_input(self, input_: FeatureInput, set_name: str = "basic_volatility") -> FeatureComputationResult:
        from usa_signal_bot.features.volatility_sets import get_volatility_indicator_set
        ind_set = get_volatility_indicator_set(set_name)
        return self.compute_for_input(input_, ind_set.indicators, ind_set.params_by_indicator)

    def compute_volatility_set_for_batch(self, batch: FeatureBatchInput, set_name: str = "basic_volatility") -> FeatureComputationResult:
        from usa_signal_bot.features.volatility_sets import get_volatility_indicator_set
        ind_set = get_volatility_indicator_set(set_name)
        return self.compute_for_batch(batch, ind_set.indicators, ind_set.params_by_indicator)

    def compute_volatility_set_from_cache(self, symbols: list[str], timeframes: list[str], set_name: str = "basic_volatility", provider_name: str = "yfinance") -> FeatureComputationResult:
        from usa_signal_bot.features.volatility_sets import get_volatility_indicator_set
        ind_set = get_volatility_indicator_set(set_name)
        return self.compute_from_cache(symbols, timeframes, ind_set.indicators, ind_set.params_by_indicator, provider_name)


    def compute_divergence_set_for_input(self, input_: FeatureInput, set_name: str = "basic_divergence") -> FeatureComputationResult:
        from usa_signal_bot.features.divergence_sets import get_divergence_indicator_set
        ind_set = get_divergence_indicator_set(set_name)
        return self.compute_for_input(input_, ind_set.indicators, ind_set.params_by_indicator)

    def compute_divergence_set_for_batch(self, batch: FeatureBatchInput, set_name: str = "basic_divergence") -> FeatureComputationResult:
        from usa_signal_bot.features.divergence_sets import get_divergence_indicator_set
        ind_set = get_divergence_indicator_set(set_name)
        return self.compute_for_batch(batch, ind_set.indicators, ind_set.params_by_indicator)

    def compute_divergence_set_from_cache(self, symbols: list[str], timeframes: list[str], set_name: str = "basic_divergence", provider_name: str = "yfinance") -> FeatureComputationResult:
        from usa_signal_bot.features.divergence_sets import get_divergence_indicator_set
        ind_set = get_divergence_indicator_set(set_name)
        return self.compute_from_cache(symbols, timeframes, ind_set.indicators, ind_set.params_by_indicator, provider_name)

    def write_result(self, result: FeatureComputationResult, fmt: FeatureStorageFormat = FeatureStorageFormat.JSONL) -> FeatureOutputMetadata:
        if not result.is_successful() or not result.feature_rows:
            raise FeatureComputationError("Cannot write unsuccessful or empty result")

        out_id = uuid.uuid4().hex
        paths = []

        group = "all"
        if len(result.request.indicator_names) == 1:
            group = result.request.indicator_names[0]

        rows_by_tf = {}
        for r in result.feature_rows:
            rows_by_tf.setdefault(r.timeframe, []).append(r)

        for tf, rows in rows_by_tf.items():
            path = build_feature_output_path(
                self.data_root, result.request.provider_name,
                result.request.universe_name, tf, group, fmt
            )
            if fmt == FeatureStorageFormat.JSONL:
                write_feature_rows_jsonl(path, rows)
            elif fmt == FeatureStorageFormat.CSV:
                write_feature_rows_csv(path, rows)
            paths.append(str(path))

        meta = FeatureOutputMetadata(
            output_id=out_id,
            provider_name=result.request.provider_name,
            universe_name=result.request.universe_name,
            symbols=result.symbols_processed,
            timeframes=result.timeframes_processed,
            indicators=result.request.indicator_names,
            produced_features=result.produced_features,
            row_count=result.row_count(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            storage_paths=paths
        )

        meta_path = build_feature_output_path(
            self.data_root, result.request.provider_name,
            result.request.universe_name, "meta", group, FeatureStorageFormat.JSONL
        ).with_name(f"{out_id}_meta.json")

        write_feature_metadata_json(meta_path, meta)

        return meta
