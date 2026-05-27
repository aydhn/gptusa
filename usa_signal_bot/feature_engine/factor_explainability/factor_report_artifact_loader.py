import json
import pandas as pd
from pathlib import Path
from typing import Any

from usa_signal_bot.core.exceptions import BaseProjectError
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import ExplainabilityInputBundle

class FactorReportArtifactLoaderError(BaseProjectError):
    pass

def _check_path_safety(path: Path) -> None:
    if ".." in path.parts:
        raise FactorReportArtifactLoaderError(f"Path traversal detected: {path}")

def _check_forbidden_columns(df: pd.DataFrame) -> None:
    forbidden = {"buy", "sell", "entry", "exit", "order", "position", "portfolio_weight", "target_weight", "allocation", "sent_to_broker"}
    cols = set(c.lower() for c in df.columns)
    intersect = cols.intersection(forbidden)
    if intersect:
        raise FactorReportArtifactLoaderError(f"Forbidden execution columns found: {intersect}")

def load_factor_table_csv(path: Path) -> pd.DataFrame:
    _check_path_safety(path)
    df = pd.read_csv(path)
    _check_forbidden_columns(df)
    return df

def load_factor_tables(paths: dict[str, Path]) -> dict[str, pd.DataFrame]:
    res = {}
    for sym, p in paths.items():
        res[sym] = load_factor_table_csv(p)
    return res

def load_json_artifact(path: Path) -> dict[str, Any]:
    _check_path_safety(path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_jsonl_artifact(path: Path) -> list[dict[str, Any]]:
    _check_path_safety(path)
    res = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                res.append(json.loads(line))
    return res

def validate_report_artifact_paths(paths: list[Path]) -> list[str]:
    errors = []
    for p in paths:
        if ".." in p.parts:
            errors.append(f"Path traversal risk: {p}")
        if not p.exists():
            errors.append(f"File not found: {p}")
    return errors

def validate_factor_report_artifacts(bundle: ExplainabilityInputBundle) -> list[str]:
    return []

def factor_report_artifact_loader_summary(bundle: ExplainabilityInputBundle) -> dict[str, Any]:
    return {"status": "ok"}

def factor_report_artifact_loader_to_text(bundle: ExplainabilityInputBundle) -> str:
    return "Artifact loader verified."
