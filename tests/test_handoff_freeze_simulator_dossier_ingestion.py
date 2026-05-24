import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_dossier_ingestion import (
    simulator_dossier_supports_handoff_freeze,
    ingest_simulator_dossier_full_review
)

def test_simulator_dossier_ingestion_valid():
    payload = {
        "simulator_dossier": {"decision": "CREATE_SIMULATOR_DOSSIER"},
        "simulator_acceptance_seal": {"status": "VALIDATED"},
        "sandbox_runtime_admission_blocker_events": [{"blocked": True, "attempt_type": "START_PAPER_SANDBOX_RUNTIME"}],
        "sandbox_runtime_admission_allowed": False
    }
    valid, warnings = simulator_dossier_supports_handoff_freeze(payload)
    assert valid is True
    assert len(warnings) == 0

def test_simulator_dossier_ingestion_invalid():
    payload = {
        "simulator_dossier": {"decision": "CREATE_SIMULATOR_DOSSIER"},
        "simulator_acceptance_seal": {"status": "VALIDATED"},
        "sandbox_runtime_admission_blocker_events": [{"blocked": False, "attempt_type": "START_PAPER_SANDBOX_RUNTIME"}],
        "sandbox_runtime_admission_allowed": True
    }
    valid, warnings = simulator_dossier_supports_handoff_freeze(payload)
    assert valid is False
    assert len(warnings) > 0
