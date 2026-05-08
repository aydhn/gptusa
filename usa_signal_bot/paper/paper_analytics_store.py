import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import os

from usa_signal_bot.paper.paper_analytics_models import (
    PaperPerformanceReport,
    paper_performance_report_to_dict
)
from usa_signal_bot.paper.paper_risk_report import PaperRiskReport, paper_risk_report_to_dict
from usa_signal_bot.paper.paper_drawdown_monitor import PaperDrawdownReport, paper_drawdown_report_to_dict
from usa_signal_bot.paper.paper_rolling_metrics import PaperRollingMetricsReport, paper_rolling_metrics_report_to_dict
from usa_signal_bot.core.exceptions import PaperAnalyticsStorageError

def paper_analytics_store_dir(data_root: Path) -> Path:
    return data_root / "paper" / "analytics"

def build_paper_analytics_run_dir(data_root: Path, report_id: str) -> Path:
    if ".." in report_id or "/" in report_id or "\\" in report_id:
        raise PaperAnalyticsStorageError(f"Invalid report_id: {report_id}")
    return paper_analytics_store_dir(data_root) / report_id

def _write_json_atomic(path: Path, data: Dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix('.tmp')
    try:
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, path)
        return path
    except Exception as e:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except:
                pass
        raise PaperAnalyticsStorageError(f"Failed to write {path}: {str(e)}")

def write_paper_performance_report_json(path: Path, report: PaperPerformanceReport) -> Path:
    return _write_json_atomic(path, paper_performance_report_to_dict(report))

def write_paper_risk_report_json(path: Path, report: PaperRiskReport) -> Path:
    return _write_json_atomic(path, paper_risk_report_to_dict(report))

def write_paper_drawdown_report_json(path: Path, report: PaperDrawdownReport) -> Path:
    return _write_json_atomic(path, paper_drawdown_report_to_dict(report))

def write_paper_rolling_metrics_report_json(path: Path, report: PaperRollingMetricsReport) -> Path:
    return _write_json_atomic(path, paper_rolling_metrics_report_to_dict(report))

def write_paper_analytics_bundle_json(path: Path, bundle: Dict[str, Any]) -> Path:
    return _write_json_atomic(path, bundle)

def read_paper_performance_report_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise PaperAnalyticsStorageError(f"File not found: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise PaperAnalyticsStorageError(f"Failed to read {path}: {str(e)}")

def list_paper_analytics_reports(data_root: Path) -> List[Path]:
    store_dir = paper_analytics_store_dir(data_root)
    if not store_dir.exists():
        return []
    return sorted([d for d in store_dir.iterdir() if d.is_dir()], key=os.path.getmtime, reverse=True)

def get_latest_paper_analytics_report_dir(data_root: Path) -> Optional[Path]:
    dirs = list_paper_analytics_reports(data_root)
    return dirs[0] if dirs else None

def paper_analytics_store_summary(data_root: Path) -> Dict[str, Any]:
    dirs = list_paper_analytics_reports(data_root)
    return {
        "store_dir": str(paper_analytics_store_dir(data_root)),
        "total_reports": len(dirs),
        "latest_report_id": dirs[0].name if dirs else None
    }
