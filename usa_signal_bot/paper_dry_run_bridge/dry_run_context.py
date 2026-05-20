from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    DryRunBridgeMode,
    create_dry_run_bridge_context_id
)
from usa_signal_bot.paper_dry_run_bridge.quarantine_ingestion import extract_quarantine_candidate_id
from usa_signal_bot.paper_dry_run_bridge.ticket_ingestion import extract_ticket_id
from usa_signal_bot.paper_dry_run_bridge.bridge_plan_ingestion import extract_bridge_plan_id
from usa_signal_bot.paper_dry_run_bridge.paper_snapshot_loader import load_read_only_paper_snapshot, redact_paper_snapshot_sensitive_fields

def build_dry_run_bridge_context(
    quarantine_payload: Optional[dict[str, Any]] = None,
    ticket_payload: Optional[dict[str, Any]] = None,
    bridge_plan_payload: Optional[dict[str, Any]] = None,
    paper_snapshot_payload: Optional[dict[str, Any]] = None
) -> DryRunBridgeContext:

    candidate_id = extract_quarantine_candidate_id(quarantine_payload) if quarantine_payload else None
    ticket_id = extract_ticket_id(ticket_payload) if ticket_payload else None
    bridge_plan_id = extract_bridge_plan_id(bridge_plan_payload) if bridge_plan_payload else None

    snapshot = load_read_only_paper_snapshot(paper_snapshot_payload)
    snapshot = redact_paper_snapshot_sensitive_fields(snapshot)
    snapshot_ref_id = snapshot.get("snapshot_id")

    warnings = []
    if not quarantine_payload:
        warnings.append("Missing quarantine payload")
    if not ticket_payload:
        warnings.append("Missing ticket payload")

    return DryRunBridgeContext(
        context_id=create_dry_run_bridge_context_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        ticket_id=ticket_id,
        bridge_plan_id=bridge_plan_id,
        paper_snapshot_ref_id=snapshot_ref_id,
        mode=DryRunBridgeMode.FULL_SUPERVISED_DRY_RUN,
        read_only_paper_snapshot=snapshot,
        candidate_metadata=quarantine_payload.get("candidate", {}) if quarantine_payload else {},
        quarantine_output_path=None,
        allow_paper_state_mutation=False,
        allow_paper_orders=False,
        allow_broker_orders=False,
        allow_telegram_real_send=False,
        allow_production_config_write=False,
        allow_active_paper_enable=False,
        warnings=warnings,
        errors=[]
    )

def build_mock_dry_run_bridge_context() -> DryRunBridgeContext:
    return build_dry_run_bridge_context()

def validate_dry_run_context_safety(context: DryRunBridgeContext) -> List[str]:
    errors = []
    if context.allow_paper_state_mutation:
        errors.append("Context allows paper state mutation.")
    if context.allow_paper_orders:
        errors.append("Context allows paper orders.")
    if context.allow_broker_orders:
        errors.append("Context allows broker orders.")
    if context.allow_telegram_real_send:
        errors.append("Context allows telegram real send.")
    if context.allow_production_config_write:
        errors.append("Context allows production config write.")
    if context.allow_active_paper_enable:
        errors.append("Context allows active paper enable.")
    return errors

def dry_run_context_summary(context: DryRunBridgeContext) -> dict[str, Any]:
    return {
        "context_id": context.context_id,
        "mode": context.mode.value,
        "candidate_id": context.candidate_id,
        "ticket_id": context.ticket_id,
        "warnings_count": len(context.warnings),
        "errors_count": len(context.errors)
    }

def dry_run_context_to_text(context: DryRunBridgeContext) -> str:
    return f"DryRun Context {context.context_id} (Mode: {context.mode.value})"
