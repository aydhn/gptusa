import pytest
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetAssemblyContext,
    MLDatasetAssemblyStatus,
    MLDatasetAssemblyDecision
)
from usa_signal_bot.ml_research.dataset_assembly.dataset_assembly_safety_validator import (
    validate_dataset_assembly_context_safety,
    dataset_assembly_text_has_trade_or_execution_language
)

def test_safety_validator_catches_unsafe_flags():
    ctx = MLDatasetAssemblyContext(
        context_id="ctx1", created_at_utc="now",
        status=MLDatasetAssemblyStatus.CREATED,
        decision=MLDatasetAssemblyDecision.RESOLVE_SOURCES,
        activation_allowed=True,
        produces_trade_signal=True,
        model_training_used=True
    )

    errors = validate_dataset_assembly_context_safety(ctx)
    assert len(errors) == 3
    assert any("activation_allowed=True" in e for e in errors)

def test_safety_validator_catches_unsafe_language():
    text = "Bu sistem otomatik olarak kesin al islemi yapar."
    assert dataset_assembly_text_has_trade_or_execution_language(text) is True

    safe_text = "This is a local metadata assembly process."
    assert dataset_assembly_text_has_trade_or_execution_language(safe_text) is False
