from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    CandidateUniverseDiagnostics, CandidateUniverseContract
)

def build_candidate_universe_diagnostics(contract: CandidateUniverseContract) -> CandidateUniverseDiagnostics:
    diag = CandidateUniverseDiagnostics()
    diag.candidate_count = contract.candidate_count
    diag.symbols = contract.symbols

    for c in contract.candidates:
        if not c.has_metric_inventory:
            diag.missing_metric_inventory_count += 1
        if not c.has_risk_notes:
            diag.missing_risk_note_count += 1
        if not c.has_robustness_evidence:
            diag.missing_robustness_evidence_count += 1

        if c.target_weight is not None or c.allocation is not None or c.position_size is not None or c.live_signal or c.order_decision:
            diag.forbidden_output_field_count += 1

    diag.diagnostics_valid = (diag.forbidden_output_field_count == 0)
    return diag

def validate_candidate_universe_diagnostics(item: CandidateUniverseDiagnostics) -> list[str]:
    errors = []
    if item.forbidden_output_field_count > 0:
        errors.append(f"Found {item.forbidden_output_field_count} candidates with forbidden output fields")
    if not item.research_data_only:
        errors.append("research_data_only must be True")
    return errors

def candidate_universe_diagnostics_summary(item: CandidateUniverseDiagnostics) -> dict[str, Any]:
    return {
        "candidate_count": item.candidate_count,
        "valid": item.diagnostics_valid,
        "forbidden_fields": item.forbidden_output_field_count
    }

def candidate_universe_diagnostics_to_text(item: CandidateUniverseDiagnostics, limit: int = 300) -> str:
    return f"CandidateUniverseDiagnostics: {item.candidate_count} candidates, {item.forbidden_output_field_count} forbidden fields"
