import pytest
from usa_signal_bot.regime_classification.validation.regime_acceptance_gate import build_regime_aware_acceptance_gate
from usa_signal_bot.regime_classification.validation.regime_alignment_ingestion import ingest_regime_alignment_review_payload
from usa_signal_bot.regime_classification.validation.compatibility_validation_runner import run_compatibility_validation
from usa_signal_bot.regime_classification.validation.phase132_models import ConditionalDiagnosticsProfile
from usa_signal_bot.core.enums import RegimeContextValidationQuality

def test_build_regime_aware_acceptance_gate():
    payload = {
        "review_id": "rev_1",
        "context": {
            "context_id": "ctx_1",
            "market_behavior_ingested": True,
            "frozen_factors_loaded": True,
            "behavior_artifacts_loaded": True,
            "alignment_specs_ready": True,
            "overlays_built": True,
            "compatibility_computed": True,
            "diagnostics_built": True,
            "readiness_gate_ready": True,
            "ready_for_phase132": True,
            "metadata_only": True,
            "research_data_only": True
        }
    }
    ingestion = ingest_regime_alignment_review_payload(payload)
    comp_res = [{"compatibility_id": "1", "score": 90, "normalized_score": 0.9, "classification": "high"}]
    over_res = [{"score": 90, "normalized_score": 0.9}]
    diag_prof = [{"profile_id": "p1"}]
    validation = run_compatibility_validation(ingestion, comp_res, over_res, diag_prof)

    prof = ConditionalDiagnosticsProfile(
        profile_id="p1",
        created_at_utc="now",
        symbol=None,
        diagnostic_count=0,
        warning_count=0,
        blocking_count=0,
        low_compatibility_diagnostic_count=0,
        uncertain_diagnostic_count=0,
        conflicted_diagnostic_count=0,
        data_quality_limited_diagnostic_count=0,
        profile_summary="",
        quality=RegimeContextValidationQuality.HIGH,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    gate = build_regime_aware_acceptance_gate(ingestion, validation, [], [prof])
    assert gate.ready_for_phase133 is True
