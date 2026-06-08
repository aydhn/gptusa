import pandas as pd
import hashlib
import json
from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingComparisonMatrix, SizingPrototypeResult

def build_sizing_comparison_matrix(results: list[SizingPrototypeResult]) -> SizingComparisonMatrix:
    matrix = SizingComparisonMatrix()
    matrix.results = results

    symbols = set(r.symbol for r in results)
    methods = set(r.method_kind.value for r in results)

    matrix.symbol_count = len(symbols)
    matrix.method_count = len(methods)
    matrix.matrix_hash = compute_sizing_comparison_matrix_hash(matrix)
    matrix.matrix_valid = len(validate_sizing_comparison_matrix(matrix)) == 0
    return matrix

def compute_sizing_comparison_matrix_hash(matrix: SizingComparisonMatrix) -> str:
    data = []
    for r in matrix.results:
        data.append({
            "symbol": r.symbol,
            "method": r.method_kind.value,
            "capped_fraction": r.capped_prototype_fraction
        })
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def sizing_comparison_matrix_to_dataframe(matrix: SizingComparisonMatrix) -> pd.DataFrame:
    data = []
    for r in matrix.results:
        data.append({
            "symbol": r.symbol,
            "method": r.method_kind.value,
            "capped_prototype_fraction": r.capped_prototype_fraction
        })
    return pd.DataFrame(data)

def validate_sizing_comparison_matrix(matrix: SizingComparisonMatrix) -> list[str]:
    errors = []
    if not matrix.research_prototype_only:
        errors.append("Matrix must be research prototype only.")
    if not matrix.no_actual_position_size:
        errors.append("Matrix must not contain actual position size.")
    if not matrix.no_target_weights:
        errors.append("Matrix must not contain target weights.")
    if not matrix.no_allocation_output:
        errors.append("Matrix must not contain allocation output.")
    if not matrix.no_order_size:
        errors.append("Matrix must not contain order size.")
    if not matrix.no_capital_allocation:
        errors.append("Matrix must not contain capital allocation.")
    return errors

def sizing_comparison_matrix_summary(matrix: SizingComparisonMatrix) -> dict[str, Any]:
    return {"symbol_count": matrix.symbol_count, "method_count": matrix.method_count, "valid": matrix.matrix_valid}

def sizing_comparison_matrix_to_text(matrix: SizingComparisonMatrix, limit: int = 300) -> str:
    return f"Sizing Comparison Matrix: {matrix.symbol_count} symbols, {matrix.method_count} methods"[:limit]
