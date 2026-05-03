"""Storage management for ranking and candidate selection reports."""

import json
from pathlib import Path
from typing import Dict, Any, List

from usa_signal_bot.core.exceptions import RankingStorageError
from usa_signal_bot.strategies.signal_ranking import SignalRankingReport
from usa_signal_bot.strategies.candidate_selection import CandidateSelectionReport, SelectedCandidate
from usa_signal_bot.core.serialization import serialize_value

def ranking_store_dir(data_root: Path) -> Path:
    d = data_root / "signals" / "ranking"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_ranking_report_path(data_root: Path, report_id: str) -> Path:
    safe_id = "".join(c for c in report_id if c.isalnum() or c in "-_")
    if not safe_id:
        raise RankingStorageError("Invalid report_id")
    return ranking_store_dir(data_root) / f"ranking_{safe_id}.json"

def build_candidate_selection_report_path(data_root: Path, report_id: str) -> Path:
    safe_id = "".join(c for c in report_id if c.isalnum() or c in "-_")
    if not safe_id:
        raise RankingStorageError("Invalid report_id")
    return ranking_store_dir(data_root) / f"selection_{safe_id}.json"

def build_portfolio_report_path(data_root: Path, run_id: str) -> Path:
    safe_id = "".join(c for c in run_id if c.isalnum() or c in "-_")
    if not safe_id:
        raise RankingStorageError("Invalid run_id")
    return ranking_store_dir(data_root) / f"portfolio_{safe_id}.json"

def build_selected_candidates_path(data_root: Path, report_id: str) -> Path:
    safe_id = "".join(c for c in report_id if c.isalnum() or c in "-_")
    if not safe_id:
        raise RankingStorageError("Invalid report_id")
    return ranking_store_dir(data_root) / f"candidates_{safe_id}.jsonl"

def write_ranking_report_json(path: Path, report: SignalRankingReport) -> Path:
    import dataclasses

    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "total_signals": report.total_signals,
        "ranked_count": report.ranked_count,
        "filtered_count": report.filtered_count,
        "top_rank_score": report.top_rank_score,
        "average_rank_score": report.average_rank_score,
        "warnings": report.warnings,
        "errors": report.errors,
        "ranked_signals": []
    }

    for rs in report.ranked_signals:
        sig_data = {
            "signal_id": rs.signal.signal_id,
            "symbol": rs.signal.symbol,
            "timeframe": rs.signal.timeframe,
            "action": rs.signal.action.value,
            "strategy_name": rs.signal.strategy_name,
            "rank_score": rs.rank_score,
            "rank": rs.rank,
            "ranking_status": rs.ranking_status.value,
            "components": rs.components,
            "penalties": rs.penalties,
            "bonuses": rs.bonuses,
            "ranking_notes": rs.ranking_notes
        }
        data["ranked_signals"].append(sig_data)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=serialize_value)

    return path

def read_ranking_report_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RankingStorageError(f"Ranking report not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def write_candidate_selection_report_json(path: Path, report: CandidateSelectionReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "total_ranked_signals": report.total_ranked_signals,
        "selected_count": report.selected_count,
        "rejected_count": report.rejected_count,
        "watchlisted_count": report.watchlisted_count,
        "warnings": report.warnings,
        "errors": report.errors,
        "selected_candidates": [],
        "rejected_candidates": []
    }

    for c in report.selected_candidates:
        c_data = {
            "candidate_id": c.candidate_id,
            "symbol": c.ranked_signal.signal.symbol,
            "timeframe": c.ranked_signal.signal.timeframe,
            "action": c.ranked_signal.signal.action.value,
            "strategy_name": c.ranked_signal.signal.strategy_name,
            "selection_status": c.selection_status.value,
            "selection_rank": c.selection_rank,
            "notes": c.notes
        }
        data["selected_candidates"].append(c_data)

    for c in report.rejected_candidates:
        c_data = {
            "candidate_id": c.candidate_id,
            "symbol": c.ranked_signal.signal.symbol,
            "timeframe": c.ranked_signal.signal.timeframe,
            "action": c.ranked_signal.signal.action.value,
            "strategy_name": c.ranked_signal.signal.strategy_name,
            "selection_status": c.selection_status.value,
            "rejection_reason": c.rejection_reason.value if c.rejection_reason else None,
            "notes": c.notes
        }
        data["rejected_candidates"].append(c_data)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=serialize_value)

    return path

def read_candidate_selection_report_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RankingStorageError(f"Candidate selection report not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def write_selected_candidates_jsonl(path: Path, candidates: List[SelectedCandidate]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    import dataclasses

    with open(path, "w") as f:
        for c in candidates:
            sig_dict = dataclasses.asdict(c.ranked_signal.signal)

            data = {
                "candidate_id": c.candidate_id,
                "selection_status": c.selection_status.value,
                "selection_rank": c.selection_rank,
                "rank_score": c.ranked_signal.rank_score,
                "notes": c.notes,
                "signal": sig_dict
            }
            f.write(json.dumps(data, default=serialize_value) + "\n")

    return path

def read_selected_candidates_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise RankingStorageError(f"Selected candidates file not found: {path}")

    candidates = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                candidates.append(json.loads(line))
    return candidates

def list_ranking_outputs(data_root: Path) -> List[Path]:
    d = ranking_store_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")) + list(d.glob("*.jsonl")), key=lambda p: p.stat().st_mtime, reverse=True)

def ranking_store_summary(data_root: Path) -> Dict[str, Any]:
    outputs = list_ranking_outputs(data_root)

    ranking_reports = [p for p in outputs if p.name.startswith("ranking_") and p.suffix == ".json"]
    selection_reports = [p for p in outputs if p.name.startswith("selection_") and p.suffix == ".json"]
    portfolio_reports = [p for p in outputs if p.name.startswith("portfolio_") and p.suffix == ".json"]
    candidate_files = [p for p in outputs if p.name.startswith("candidates_") and p.suffix == ".jsonl"]

    return {
        "total_files": len(outputs),
        "ranking_reports": len(ranking_reports),
        "selection_reports": len(selection_reports),
        "portfolio_reports": len(portfolio_reports),
        "candidate_files": len(candidate_files),
        "latest_file": outputs[0].name if outputs else None
    }
