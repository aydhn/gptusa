import pytest
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import *

def test_models_exist():
    assert LocalPaperAdmissionSimulatorGateDossier is not None
    assert SimulatorAcceptanceSeal is not None
    assert PaperSandboxRuntimeAdmissionBlockerRule is not None
    assert PaperSandboxRuntimeAdmissionBlockerEvent is not None

def test_safety_flags():
    assert SimulatorDossierRiskFlag.BROKER_ORDER_RISK.value == "BROKER_ORDER_RISK"

def test_sandbox_runtime_admission_blocker_default():
    from usa_signal_bot.local_paper_admission_simulator_dossier.final_sandbox_runtime_admission_blocker import FinalPaperSandboxRuntimeAdmissionBlocker
    blocker = FinalPaperSandboxRuntimeAdmissionBlocker()
    attempt = blocker.evaluate_attempt(PaperSandboxRuntimeAdmissionAttemptType.START_PAPER_SANDBOX_RUNTIME)
    assert attempt.blocked is True
    assert attempt.active_paper_enabled is False

def test_simulator_acceptance_seal_default():
    from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_acceptance_seal import build_default_simulator_acceptance_seal
    seal = build_default_simulator_acceptance_seal()
    assert seal.allows_active_paper is False
    assert seal.allows_broker_execution is False

def test_simulator_dossier_builder():
    from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier import build_local_paper_admission_simulator_gate_dossier
    dossier = build_local_paper_admission_simulator_gate_dossier({})
    assert dossier.sealed is True
    assert dossier.immutable is True
    assert dossier.activation_allowed is False
    assert dossier.allows_active_paper is False

def test_simulator_dossier_validation():
    from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_validation import validate_no_live_execution_language_in_simulator_dossier
    report = validate_no_live_execution_language_in_simulator_dossier("sent to broker")
    assert report.valid is False
    assert len(report.errors) == 1
