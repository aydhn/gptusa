from typing import List, Dict, Any, Optional
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalClosureContext,
    FinalClosureFullReview,
    FinalClosureReportType,
    FinalClosureStatus,
    FinalClosureDecision,
    create_final_closure_context_id,
    create_final_closure_full_review_id,
    generate_timestamp
)
from usa_signal_bot.release.final_closure.phase159_handoff_ingestion import ingest_latest_phase160_handoff_package_from_store
from usa_signal_bot.release.final_closure.final_input_resolver import build_final_input_references
from usa_signal_bot.release.final_closure.final_artifact_index import build_final_artifact_index
from usa_signal_bot.release.final_closure.final_phase_lineage import build_final_phase_lineage
from usa_signal_bot.release.final_closure.final_system_audit_checklist import build_final_system_audit_checklist
from usa_signal_bot.release.final_closure.final_system_audit_report import build_final_system_audit_report
from usa_signal_bot.release.final_closure.final_safety_closure import build_final_safety_closure
from usa_signal_bot.release.final_closure.final_limitation_register import build_final_limitation_register
from usa_signal_bot.release.final_closure.final_documentation_index import build_final_documentation_index
from usa_signal_bot.release.final_closure.final_runbook_index import build_final_runbook_index
from usa_signal_bot.release.final_closure.final_test_evidence_summary import build_final_test_evidence_summary
from usa_signal_bot.release.final_closure.final_quality_observability_summary import build_final_quality_observability_summary
from usa_signal_bot.release.final_closure.final_delivery_certificate import build_final_delivery_certificate
from usa_signal_bot.release.final_closure.project_closure_report import build_project_closure_report
from usa_signal_bot.release.final_closure.project_closure_manifest import build_project_closure_manifest
from usa_signal_bot.release.final_closure.final_safety_boundary import build_final_safety_boundary_rules, build_final_safety_boundary_result
from usa_signal_bot.release.final_closure.final_closure_readiness_gate import build_final_closure_readiness_gate
from pathlib import Path

def build_final_closure_context(data_root: Optional[Path] = None, unsafe_test: bool = False) -> FinalClosureContext:
    if data_root is None:
        data_root = Path("data")

    context = FinalClosureContext(
        context_id=create_final_closure_context_id(),
        created_at_utc=generate_timestamp(),
        status=FinalClosureStatus.CREATED,
        decision=FinalClosureDecision.LOAD_PHASE160_HANDOFF_PACKAGE
    )

    # 1. Ingestion
    ingest = ingest_latest_phase160_handoff_package_from_store(data_root)
    context.ingestion = ingest
    context.phase160_handoff_ingested = True
    context.status = FinalClosureStatus.PHASE160_HANDOFF_INGESTED

    # 2. Inputs
    dummy_payloads = {"phase160_handoff_package": {"valid": True}}
    if unsafe_test:
        dummy_payloads["phase160_handoff_package"]["broker_order"] = True
    context.input_references = build_final_input_references(dummy_payloads)
    context.inputs_resolved = True
    context.status = FinalClosureStatus.INPUTS_RESOLVED

    # 3. Artifact Index
    context.artifact_index = build_final_artifact_index()
    context.final_artifact_index_built = True
    context.status = FinalClosureStatus.FINAL_ARTIFACT_INDEX_BUILT

    # 4. Phase Lineage
    context.phase_lineage = build_final_phase_lineage()
    context.final_phase_lineage_built = True
    context.status = FinalClosureStatus.FINAL_PHASE_LINEAGE_BUILT

    # 5. Audit Checklist
    context.final_audit_checklist = build_final_system_audit_checklist(context.artifact_index, context.phase_lineage)
    context.final_system_audit_checklist_built = True
    context.status = FinalClosureStatus.FINAL_SYSTEM_AUDIT_CHECKLIST_BUILT

    # 6. Audit Report
    context.final_audit_report = build_final_system_audit_report(context.final_audit_checklist, context.artifact_index, context.phase_lineage)
    context.final_system_audit_report_built = True
    context.status = FinalClosureStatus.FINAL_SYSTEM_AUDIT_REPORT_BUILT

    # 7. Safety Closure
    context.final_safety_closure = build_final_safety_closure({"unsafe": unsafe_test})
    context.final_safety_closure_built = True
    context.status = FinalClosureStatus.FINAL_SAFETY_CLOSURE_BUILT

    # 8. Limitation Register
    context.limitation_register = build_final_limitation_register()
    context.final_limitation_register_built = True
    context.status = FinalClosureStatus.FINAL_LIMITATION_REGISTER_BUILT

    # 9. Docs
    context.documentation_index = build_final_documentation_index()
    context.final_documentation_index_built = True
    context.status = FinalClosureStatus.FINAL_DOCUMENTATION_INDEX_BUILT

    # 10. Runbooks
    context.runbook_index = build_final_runbook_index()
    context.final_runbook_index_built = True
    context.status = FinalClosureStatus.FINAL_RUNBOOK_INDEX_BUILT

    # 11. Tests
    context.test_evidence_summary = build_final_test_evidence_summary()
    context.final_test_evidence_summary_built = True
    context.status = FinalClosureStatus.FINAL_TEST_EVIDENCE_SUMMARY_BUILT

    # 12. Quality
    context.quality_observability_summary = build_final_quality_observability_summary()
    context.final_quality_observability_summary_built = True
    context.status = FinalClosureStatus.FINAL_QUALITY_OBSERVABILITY_SUMMARY_BUILT

    # 13. Delivery Cert
    context.final_delivery_certificate = build_final_delivery_certificate(context.final_audit_report, context.final_safety_closure, context.limitation_register)
    context.final_delivery_certificate_built = True
    context.status = FinalClosureStatus.FINAL_DELIVERY_CERTIFICATE_BUILT

    # 14. Project Closure Report
    context.project_closure_report = build_project_closure_report(
        context.final_delivery_certificate,
        context.final_audit_report,
        context.final_safety_closure,
        context.limitation_register,
        context.documentation_index,
        context.runbook_index,
        context.test_evidence_summary,
        context.quality_observability_summary
    )
    context.project_closure_report_built = True
    context.status = FinalClosureStatus.PROJECT_CLOSURE_REPORT_BUILT

    # 15. Safety Boundary
    rules = build_final_safety_boundary_rules({"unsafe": unsafe_test})
    context.final_safety_boundary = build_final_safety_boundary_result(rules)
    context.final_safety_boundary_validated = True
    context.status = FinalClosureStatus.FINAL_SAFETY_BOUNDARY_VALIDATED

    # 16. Manifest
    context.project_closure_manifest = build_project_closure_manifest(context.project_closure_report)
    context.project_closure_manifest_built = True
    context.status = FinalClosureStatus.PROJECT_CLOSURE_MANIFEST_BUILT

    # 17. Readiness Gate
    context.final_closure_readiness_gate = build_final_closure_readiness_gate(
        context.final_audit_report,
        context.final_delivery_certificate,
        context.project_closure_report,
        context.project_closure_manifest,
        context.final_safety_boundary
    )
    context.final_closure_readiness_gate_built = True
    context.final_closure_readiness_gate_passed = context.final_closure_readiness_gate.status.value == "PASSED"
    context.status = FinalClosureStatus.FINAL_CLOSURE_READINESS_GATE_BUILT

    # Finalize
    if context.final_closure_readiness_gate_passed:
        context.project_closed = True
        context.status = FinalClosureStatus.PROJECT_CLOSED
        context.decision = FinalClosureDecision.CLOSE_PROJECT
    else:
        context.status = FinalClosureStatus.BLOCKED
        context.decision = FinalClosureDecision.BLOCK
        context.errors.append("Project closure blocked by readiness gate.")

    return context

def build_final_closure_full_review(data_root: Optional[Path] = None, unsafe_test: bool = False) -> FinalClosureFullReview:
    context = build_final_closure_context(data_root, unsafe_test)

    return FinalClosureFullReview(
        review_id=create_final_closure_full_review_id(),
        created_at_utc=generate_timestamp(),
        report_type=FinalClosureReportType.FULL_PHASE160_REVIEW,
        ingestion=context.ingestion,
        context=context,
        final_audit_report=context.final_audit_report,
        final_delivery_certificate=context.final_delivery_certificate,
        project_closure_report=context.project_closure_report,
        project_closure_manifest=context.project_closure_manifest,
        final_closure_readiness_gate=context.final_closure_readiness_gate,
        warnings=context.warnings,
        errors=context.errors
    )

def final_closure_full_review_summary(review: FinalClosureFullReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "project_closed": review.project_closure_manifest.project_closed,
        "readiness_gate_passed": review.final_closure_readiness_gate.status.value == "PASSED"
    }

def final_closure_limitations_text() -> str:
    return "Phase 160 is a final system audit and project closure phase. It is not a deployment phase. It is not live trading, paper trading, or broker execution. Output is not investment advice."

def final_closure_full_review_to_text(review: FinalClosureFullReview, limit: int = 300) -> str:
    return f"Final Closure Full Review: Closed={review.project_closure_manifest.project_closed}, Errors={len(review.errors)}"
