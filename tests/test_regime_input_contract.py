from usa_signal_bot.regime_classification.foundation.regime_input_contract import (
    build_regime_input_contract,
    validate_regime_input_contract
)
from usa_signal_bot.regime_classification.foundation.phase126_models import RegimeResearchInputBundle

def test_build_regime_input_contract():
    bundle = RegimeResearchInputBundle(
        bundle_id="bnd_123",
        created_at_utc="",
        source_final_closure_review_id=None,
        frozen_artifacts=[],
        factor_table_refs=["ref1"],
        factor_diagnostics_refs=["ref2"],
        schema_contract_refs=["ref3"],
        lineage_contract_refs=["ref4"],
        safety_contract_refs=["ref5"],
        research_report_refs=["ref6"],
        bundle_valid=True,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    contract = build_regime_input_contract(bundle)
    assert contract["bundle_id"] == "bnd_123"
    assert contract["allowed_use"] == "regime_research_only"
    assert "trade_signal" in contract["disallowed_use"]

def test_validate_regime_input_contract_invalid():
    contract = {
        "bundle_id": "bnd_123",
        "allowed_use": "trade_execution", # Invalid
        "disallowed_use": ["order_decision"] # Missing required items
    }
    errors = validate_regime_input_contract(contract)
    assert len(errors) > 1
    assert any("allowed_use must be" in e for e in errors)
    assert any("trade_signal" in e for e in errors)
