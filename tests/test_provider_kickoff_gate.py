
from usa_signal_bot.core_runtime_acceptance.provider_expansion_kickoff_gate import build_data_provider_expansion_kickoff_gate
from usa_signal_bot.core_runtime_acceptance.core_runtime_acceptance import build_core_runtime_acceptance_report
from usa_signal_bot.core_runtime_acceptance.foundation_freeze import build_advanced_foundation_freeze_bundle
from usa_signal_bot.core_runtime_acceptance.phase105_models import LifecycleReviewIngestionResult

def test_kickoff_gate():
    lifecycle = LifecycleReviewIngestionResult("lri", "now", valid_for_phase105=True)
    report = build_core_runtime_acceptance_report(lifecycle, [])
    freeze = build_advanced_foundation_freeze_bundle([])

    gate = build_data_provider_expansion_kickoff_gate(report, freeze)
    assert gate.ready_for_phase106 == True
    assert gate.provider_ready == True
    assert gate.metadata_only == True
    assert gate.activation_allowed == False
