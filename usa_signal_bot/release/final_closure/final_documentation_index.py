from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalDocumentationIndex,
    create_final_documentation_index_id,
    generate_timestamp
)
import hashlib
import json

def default_required_final_docs() -> List[str]:
    return [
        "docs/PHASE_160_FINAL_SYSTEM_AUDIT_AND_PROJECT_CLOSURE.md",
        "docs/PHASE160_INPUTS_AND_BOUNDARIES.md",
        "docs/FINAL_ARTIFACT_INDEX.md",
        "docs/FINAL_PHASE_LINEAGE.md",
        "docs/FINAL_SYSTEM_AUDIT_CHECKLIST.md",
        "docs/FINAL_SYSTEM_AUDIT_REPORT.md",
        "docs/FINAL_SAFETY_CLOSURE.md",
        "docs/FINAL_LIMITATION_REGISTER.md",
        "docs/FINAL_DOCUMENTATION_AND_RUNBOOK_INDEX.md",
        "docs/FINAL_TEST_EVIDENCE_SUMMARY.md",
        "docs/FINAL_QUALITY_OBSERVABILITY_SUMMARY.md",
        "docs/FINAL_DELIVERY_CERTIFICATE.md",
        "docs/PROJECT_CLOSURE_REPORT.md",
        "docs/PROJECT_CLOSURE_MANIFEST.md",
        "docs/FINAL_SAFETY_BOUNDARY.md",
        "docs/PHASE_160_LIMITATIONS.md",
        "docs/PHASE_160_SUMMARY.md",
        "docs/PROJECT_FINAL_STATUS.md"
    ]

def compute_final_documentation_index_hash(index: FinalDocumentationIndex) -> str:
    state = {
        "doc_paths": sorted(index.doc_paths),
        "required_docs": sorted(index.required_docs),
        "missing_required_docs": sorted(index.missing_required_docs)
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_documentation_index() -> FinalDocumentationIndex:
    required = default_required_final_docs()
    # Assume all available for this phase
    available = required.copy()
    missing = []

    index = FinalDocumentationIndex(
        index_id=create_final_documentation_index_id(),
        created_at_utc=generate_timestamp(),
        doc_paths=available,
        required_docs=required,
        available_required_docs=available,
        missing_required_docs=missing,
        index_valid=len(missing) == 0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    index.index_hash = compute_final_documentation_index_hash(index)
    return index

def validate_final_documentation_index(index: FinalDocumentationIndex) -> List[str]:
    errors = []
    if not index.index_valid:
        errors.append(f"Missing required docs: {index.missing_required_docs}")
    return errors

def final_documentation_index_to_text(index: FinalDocumentationIndex, limit: int = 300) -> str:
    return f"Final Documentation Index: Valid={index.index_valid}, Missing={len(index.missing_required_docs)}"
