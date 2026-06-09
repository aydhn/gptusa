from typing import Any, Dict, List, Optional
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    AcceptanceEvidenceBundle,
    AcceptanceEvidenceItem,
    AcceptanceScenarioMatrix,
    AdvancedDryRunStep,
    create_acceptance_evidence_bundle_id,
    create_acceptance_evidence_item_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_acceptance_evidence_items(matrix: AcceptanceScenarioMatrix, steps: List[AdvancedDryRunStep]) -> List[AcceptanceEvidenceItem]:
    items = []

    # In a real run, this would load actual files. For this phase we generate safe mocks for valid steps.
    for step in steps:
        if step.evidence_ref:
            items.append(AcceptanceEvidenceItem(
                evidence_id=create_acceptance_evidence_item_id(),
                created_at_utc=generate_timestamp(),
                area_kind=step.area_kind,
                scenario_id=step.scenario_id,
                evidence_name=step.evidence_ref,
                evidence_type="json",
                evidence_hash=hashlib.sha256(step.evidence_ref.encode()).hexdigest(),
                available=True,
                valid=True,
                read_only=True,
                local_only=True,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            ))

    return items

def compute_acceptance_evidence_bundle_hash(bundle: AcceptanceEvidenceBundle) -> str:
    data = []
    for item in bundle.evidence_items:
        data.append({
            "name": item.evidence_name,
            "hash": item.evidence_hash
        })
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def validate_acceptance_evidence_bundle(bundle: AcceptanceEvidenceBundle) -> List[str]:
    errors = []
    if not bundle.bundle_valid:
        errors.append("Bundle is marked invalid")
    if bundle.missing_required_count > 0:
        errors.append(f"Missing {bundle.missing_required_count} required evidence items")
    if not bundle.read_only:
        errors.append("Bundle must be read_only")
    if not bundle.local_only:
        errors.append("Bundle must be local_only")
    return errors

def build_acceptance_evidence_bundle(matrix: AcceptanceScenarioMatrix, steps: List[AdvancedDryRunStep]) -> AcceptanceEvidenceBundle:
    items = build_acceptance_evidence_items(matrix, steps)

    # calculate required count from scenarios
    required_count = 0
    for s in matrix.scenarios:
        if s.required:
            required_count += len(s.expected_evidence)

    bundle = AcceptanceEvidenceBundle(
        bundle_id=create_acceptance_evidence_bundle_id(),
        created_at_utc=generate_timestamp(),
        evidence_items=items,
        evidence_count=len(items),
        required_evidence_count=required_count,
        available_required_count=len(items), # Simplified
        missing_required_count=max(0, required_count - len(items)),
        bundle_hash=None,
        bundle_valid=True,
        read_only=True,
        local_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    bundle.bundle_hash = compute_acceptance_evidence_bundle_hash(bundle)

    if bundle.missing_required_count > 0:
        bundle.risk_flags.append(AdvancedAcceptanceRiskFlag.EVIDENCE_BUNDLE_INVALID)
        bundle.bundle_valid = False

    return bundle

def acceptance_evidence_bundle_to_text(bundle: AcceptanceEvidenceBundle, limit: int = 300) -> str:
    lines = [f"Evidence Bundle: {bundle.bundle_id}", f"Valid: {bundle.bundle_valid}"]
    for e in bundle.evidence_items[:limit]:
        lines.append(f" - {e.evidence_name} [{e.evidence_type}]")
    return "\n".join(lines)
