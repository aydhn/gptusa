from typing import Any, Tuple, Optional
from datetime import datetime, timezone
import hashlib
import json
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import ZeroMutationBaseline, create_zero_mutation_baseline_id

def collect_zero_mutation_baseline(paper_payload: Optional[dict[str, Any]] = None, baseline_type: str = "before") -> ZeroMutationBaseline:
    payload = paper_payload or {}
    return ZeroMutationBaseline(
        baseline_id=create_zero_mutation_baseline_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=payload.get("candidate_id"),
        baseline_type=baseline_type,
        paper_snapshot_hash=stable_paper_snapshot_hash(payload),
        paper_snapshot_summary={},
        paper_state_committed=False,
        paper_order_executed=False,
        portfolio_state_mutated=False,
        position_mutated=False,
        cash_mutated=False,
        equity_mutated=False,
        config_patched=False,
        broker_order_sent=False,
        telegram_real_sent=False,
        warnings=[],
        errors=[]
    )

def collect_before_after_zero_mutation_baselines(before_payload: Optional[dict[str, Any]] = None, after_payload: Optional[dict[str, Any]] = None) -> Tuple[ZeroMutationBaseline, ZeroMutationBaseline]:
    return (
        collect_zero_mutation_baseline(before_payload, "before"),
        collect_zero_mutation_baseline(after_payload, "after")
    )

def stable_paper_snapshot_hash(snapshot: dict[str, Any]) -> str:
    redacted = redact_zero_mutation_baseline_sensitive_fields(snapshot)
    return hashlib.sha256(json.dumps(redacted, sort_keys=True).encode()).hexdigest()

def redact_zero_mutation_baseline_sensitive_fields(snapshot: dict[str, Any]) -> dict[str, Any]:
    return snapshot.copy()

def zero_mutation_baseline_summary(baseline: ZeroMutationBaseline) -> dict[str, Any]:
    return {
        "id": baseline.baseline_id,
        "type": baseline.baseline_type,
        "hash": baseline.paper_snapshot_hash
    }

def zero_mutation_baseline_to_text(baseline: ZeroMutationBaseline) -> str:
    return f"ZeroMutationBaseline {baseline.baseline_type} hash {baseline.paper_snapshot_hash}"
