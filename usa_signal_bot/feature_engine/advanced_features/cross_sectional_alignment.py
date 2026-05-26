import pandas as pd
from typing import List, Dict, Any, Tuple
from pathlib import Path
from usa_signal_bot.core.exceptions import CrossSectionalAlignmentError
from usa_signal_bot.core.enums import CrossSectionalAlignmentStatus, AdvancedFeatureRiskFlag
from usa_signal_bot.feature_engine.advanced_features.phase118_models import CrossSectionalAlignmentResult, create_cross_sectional_alignment_id
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def load_symbol_feature_tables(paths: Dict[str, Path]) -> Dict[str, pd.DataFrame]:
    """Loads feature tables from given paths."""
    tables = {}
    for symbol, p in paths.items():
        if p.exists():
            df = pd.read_csv(p)
            tables[symbol] = df
    return tables

def common_timestamps(tables: Dict[str, pd.DataFrame], timestamp_col: str = "timestamp") -> List[str]:
    """Finds intersection of timestamps across all dataframes."""
    if not tables:
        return []

    intersect_ts = None
    for sym, df in tables.items():
        if timestamp_col not in df.columns:
            continue
        ts_set = set(df[timestamp_col].astype(str).tolist())
        if intersect_ts is None:
            intersect_ts = ts_set
        else:
            intersect_ts = intersect_ts.intersection(ts_set)

    if intersect_ts is None:
        return []

    return sorted(list(intersect_ts))

def align_feature_tables_by_timestamp(tables: Dict[str, pd.DataFrame], timestamp_col: str = "timestamp") -> Tuple[Dict[str, pd.DataFrame], CrossSectionalAlignmentResult]:
    """Aligns tables by intersection of timestamps."""
    intersect_ts = common_timestamps(tables, timestamp_col)

    aligned_tables = {}
    missing_symbols = []
    timestamp_mismatches = 0

    for sym, df in tables.items():
        if timestamp_col not in df.columns:
            missing_symbols.append(sym)
            continue

        # Filter down
        original_len = len(df)
        df_aligned = df[df[timestamp_col].astype(str).isin(intersect_ts)].copy()

        timestamp_mismatches += (original_len - len(df_aligned))
        aligned_tables[sym] = df_aligned.sort_values(timestamp_col).reset_index(drop=True)

    status = CrossSectionalAlignmentStatus.ALIGNED
    warnings = []
    if missing_symbols:
        status = CrossSectionalAlignmentStatus.PARTIALLY_ALIGNED
        warnings.append(f"Missing timestamp col for {missing_symbols}")
    if len(aligned_tables) < 2:
        status = CrossSectionalAlignmentStatus.BLOCKED

    result = CrossSectionalAlignmentResult(
        alignment_id=create_cross_sectional_alignment_id(),
        created_at_utc=_now(),
        universe_id=None,
        symbols=list(aligned_tables.keys()),
        aligned_timestamps=intersect_ts,
        input_table_count=len(tables),
        aligned_table_count=len(aligned_tables),
        missing_symbol_count=len(missing_symbols),
        timestamp_mismatch_count=timestamp_mismatches,
        status=status,
        warnings=warnings,
        errors=[],
        risk_flags=[],
        metadata={}
    )

    return aligned_tables, result

def validate_cross_sectional_alignment(tables: Dict[str, pd.DataFrame]) -> List[str]:
    errors = []
    if len(tables) < 2:
        errors.append("Need at least 2 tables for alignment.")

    ts = common_timestamps(tables)
    if not ts:
        errors.append("No common timestamps found across tables.")

    return errors

def cross_sectional_alignment_summary(result: CrossSectionalAlignmentResult) -> Dict[str, Any]:
    return {
        "status": result.status.value,
        "aligned_table_count": result.aligned_table_count,
        "common_timestamp_count": len(result.aligned_timestamps)
    }

def cross_sectional_alignment_to_text(result: CrossSectionalAlignmentResult) -> str:
    return f"Alignment {result.alignment_id}: {result.aligned_table_count} tables, {len(result.aligned_timestamps)} timestamps [{result.status.value}]"
