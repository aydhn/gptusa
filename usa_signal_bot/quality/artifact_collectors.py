"""Quality artifact collectors for USA Signal Bot."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import ArtifactFreshnessStatus
from usa_signal_bot.core.exceptions import ArtifactCollectionError

@dataclass
class QualityArtifactIndex:
    created_at_utc: str
    data_root: str
    latest_scan_run_dir: Optional[str]
    latest_backtest_run_dir: Optional[str]
    latest_basket_run_dir: Optional[str]
    latest_risk_run_dir: Optional[str]
    latest_portfolio_run_dir: Optional[str]
    latest_paper_run_dir: Optional[str]
    latest_paper_analytics_dir: Optional[str]
    latest_comparison_run_dir: Optional[str]
    latest_notification_run_dir: Optional[str]
    latest_alert_eval_dir: Optional[str]
    artifact_count: int
    warnings: List[str]
    errors: List[str]

def load_json_if_exists(path: Optional[Path]) -> Optional[Dict[str, Any]]:
    if not path or not path.exists() or not path.is_file():
        return None
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return None

def load_jsonl_if_exists(path: Optional[Path], limit: Optional[int] = None) -> List[Dict[str, Any]]:
    if not path or not path.exists() or not path.is_file():
        return []
    res = []
    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    res.append(json.loads(line))
                    if limit is not None and len(res) >= limit:
                        break
                except Exception:
                    pass
    except Exception:
        pass
    return res

def _find_latest_dir(base_dir: Path) -> Optional[Path]:
    if not base_dir.exists() or not base_dir.is_dir():
        return None
    dirs = [d for d in base_dir.iterdir() if d.is_dir()]
    if not dirs:
        return None
    dirs.sort(key=lambda p: p.name, reverse=True)
    return dirs[0]

def collect_quality_artifact_index(data_root: Path) -> QualityArtifactIndex:
    warnings = []
    errors = []

    if not data_root.exists():
        warnings.append(f"Data root {data_root} does not exist.")

    scan_dir = _find_latest_dir(data_root / "scans")
    backtest_dir = _find_latest_dir(data_root / "backtests")
    basket_dir = _find_latest_dir(data_root / "portfolio" / "baskets")
    risk_dir = _find_latest_dir(data_root / "risk" / "decisions")
    portfolio_dir = _find_latest_dir(data_root / "portfolio" / "allocations")
    paper_dir = _find_latest_dir(data_root / "paper" / "runs")
    analytics_dir = _find_latest_dir(data_root / "paper" / "analytics")
    comparison_dir = _find_latest_dir(data_root / "comparison" / "runs")
    notification_dir = _find_latest_dir(data_root / "notifications")
    alert_eval_dir = _find_latest_dir(data_root / "alerts")

    count = sum(1 for d in [scan_dir, backtest_dir, basket_dir, risk_dir, portfolio_dir, paper_dir, analytics_dir, comparison_dir, notification_dir, alert_eval_dir] if d is not None)

    return QualityArtifactIndex(
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        data_root=str(data_root),
        latest_scan_run_dir=str(scan_dir) if scan_dir else None,
        latest_backtest_run_dir=str(backtest_dir) if backtest_dir else None,
        latest_basket_run_dir=str(basket_dir) if basket_dir else None,
        latest_risk_run_dir=str(risk_dir) if risk_dir else None,
        latest_portfolio_run_dir=str(portfolio_dir) if portfolio_dir else None,
        latest_paper_run_dir=str(paper_dir) if paper_dir else None,
        latest_paper_analytics_dir=str(analytics_dir) if analytics_dir else None,
        latest_comparison_run_dir=str(comparison_dir) if comparison_dir else None,
        latest_notification_run_dir=str(notification_dir) if notification_dir else None,
        latest_alert_eval_dir=str(alert_eval_dir) if alert_eval_dir else None,
        artifact_count=count,
        warnings=warnings,
        errors=errors
    )

def quality_artifact_index_to_dict(index: QualityArtifactIndex) -> dict:
    return {
        "created_at_utc": index.created_at_utc,
        "data_root": index.data_root,
        "latest_scan_run_dir": index.latest_scan_run_dir,
        "latest_backtest_run_dir": index.latest_backtest_run_dir,
        "latest_basket_run_dir": index.latest_basket_run_dir,
        "latest_risk_run_dir": index.latest_risk_run_dir,
        "latest_portfolio_run_dir": index.latest_portfolio_run_dir,
        "latest_paper_run_dir": index.latest_paper_run_dir,
        "latest_paper_analytics_dir": index.latest_paper_analytics_dir,
        "latest_comparison_run_dir": index.latest_comparison_run_dir,
        "latest_notification_run_dir": index.latest_notification_run_dir,
        "latest_alert_eval_dir": index.latest_alert_eval_dir,
        "artifact_count": index.artifact_count,
        "warnings": index.warnings,
        "errors": index.errors,
    }

def load_latest_quality_artifacts(data_root: Path) -> Dict[str, Any]:
    index = collect_quality_artifact_index(data_root)
    artifacts = {"index": index}

    if index.latest_scan_run_dir:
        d = Path(index.latest_scan_run_dir)
        artifacts["scan_summary"] = load_json_if_exists(d / "scan_summary.json")
        artifacts["scan_signals"] = load_jsonl_if_exists(d / "signals.jsonl")
        artifacts["scan_candidates"] = load_jsonl_if_exists(d / "candidates.jsonl")

    if index.latest_backtest_run_dir:
        d = Path(index.latest_backtest_run_dir)
        artifacts["backtest_summary"] = load_json_if_exists(d / "backtest_summary.json")
        artifacts["backtest_metrics"] = load_json_if_exists(d / "metrics.json")

    if index.latest_risk_run_dir:
        artifacts["risk_summary"] = load_json_if_exists(Path(index.latest_risk_run_dir) / "risk_summary.json")
        artifacts["risk_decisions"] = load_jsonl_if_exists(Path(index.latest_risk_run_dir) / "risk_decisions.jsonl")

    if index.latest_portfolio_run_dir:
        artifacts["portfolio_summary"] = load_json_if_exists(Path(index.latest_portfolio_run_dir) / "portfolio_summary.json")
        artifacts["portfolio_allocations"] = load_jsonl_if_exists(Path(index.latest_portfolio_run_dir) / "allocations.jsonl")

    if index.latest_paper_run_dir:
        artifacts["paper_summary"] = load_json_if_exists(Path(index.latest_paper_run_dir) / "paper_summary.json")

    if index.latest_comparison_run_dir:
        artifacts["comparison_summary"] = load_json_if_exists(Path(index.latest_comparison_run_dir) / "comparison_summary.json")

    artifacts["data_root"] = str(data_root)
    return artifacts

def artifact_freshness_status(path: Optional[Path], max_age_hours: Optional[int] = None) -> ArtifactFreshnessStatus:
    if not path or not path.exists():
        return ArtifactFreshnessStatus.MISSING
    if not max_age_hours:
        return ArtifactFreshnessStatus.FRESH

    try:
        mtime = path.stat().st_mtime
        age = (datetime.now().timestamp() - mtime) / 3600.0
        if age > max_age_hours:
            return ArtifactFreshnessStatus.STALE
        return ArtifactFreshnessStatus.FRESH
    except Exception:
        return ArtifactFreshnessStatus.UNKNOWN

def summarize_artifacts_for_quality(index: QualityArtifactIndex) -> Dict[str, Any]:
    return quality_artifact_index_to_dict(index)

def quality_artifact_index_to_text(index: QualityArtifactIndex) -> str:
    lines = [
        f"Quality Artifact Index (count: {index.artifact_count})",
        f"Scan: {index.latest_scan_run_dir or 'Missing'}",
        f"Backtest: {index.latest_backtest_run_dir or 'Missing'}",
        f"Paper: {index.latest_paper_run_dir or 'Missing'}",
        f"Comparison: {index.latest_comparison_run_dir or 'Missing'}"
    ]
    if index.warnings:
        lines.append(f"Warnings: {len(index.warnings)}")
    return "\n".join(lines)
