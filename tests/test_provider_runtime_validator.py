from usa_signal_bot.data_provider_runtime.provider_runtime_validator import validate_provider_runtime_context_safety
from usa_signal_bot.data_provider_runtime.provider_runtime_report import build_provider_runtime_context

def test_provider_runtime_validator():
    ctx = build_provider_runtime_context()
    ctx.ingestion.provider_abstraction_ready = True
    ctx.ingestion.metadata_only = True
    ctx.ingestion.provider_network_fetch_enabled_now = False
    errors = validate_provider_runtime_context_safety(ctx)
    assert len(errors) == 0
