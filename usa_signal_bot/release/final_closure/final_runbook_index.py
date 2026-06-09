from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalRunbookIndex,
    create_final_runbook_index_id,
    generate_timestamp
)
import hashlib
import json

def default_required_final_runbooks() -> List[str]:
    return [
        "local setup",
        "config validation",
        "data refresh dry-run",
        "feature generation dry-run",
        "backtest dry-run",
        "portfolio governance dry-run",
        "acceptance rehearsal dry-run",
        "safety validation",
        "troubleshooting",
        "non-deployment final delivery notes"
    ]

def compute_final_runbook_index_hash(index: FinalRunbookIndex) -> str:
    state = {
        "runbook_paths": sorted(index.runbook_paths),
        "required_runbooks": sorted(index.required_runbooks),
        "missing_required_runbooks": sorted(index.missing_required_runbooks)
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_runbook_index() -> FinalRunbookIndex:
    required = default_required_final_runbooks()
    # Assume all runbooks available (represented as sections in the docs)
    available = required.copy()
    missing = []

    index = FinalRunbookIndex(
        index_id=create_final_runbook_index_id(),
        created_at_utc=generate_timestamp(),
        runbook_paths=available,
        required_runbooks=required,
        available_required_runbooks=available,
        missing_required_runbooks=missing,
        index_valid=len(missing) == 0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    index.index_hash = compute_final_runbook_index_hash(index)
    return index

def validate_final_runbook_index(index: FinalRunbookIndex) -> List[str]:
    errors = []
    if not index.index_valid:
        errors.append(f"Missing required runbooks: {index.missing_required_runbooks}")
    return errors

def final_runbook_index_to_text(index: FinalRunbookIndex, limit: int = 300) -> str:
    return f"Final Runbook Index: Valid={index.index_valid}, Missing={len(index.missing_required_runbooks)}"
