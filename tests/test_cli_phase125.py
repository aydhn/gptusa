import pytest
from types import SimpleNamespace
import usa_signal_bot.app.cli as cli

def test_final_closure_info(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_info(args)
    captured = capsys.readouterr()
    assert "Phase 125" in captured.out
    assert "NOT an active paper trading or deployment phase" in captured.out

def test_final_closure_ingest_freeze_prep(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_ingest_freeze_prep(args)
    captured = capsys.readouterr()
    assert "FreezePrepIngestion" in captured.out

def test_final_artifact_chain_load(capsys):
    args = SimpleNamespace(write=False)
    cli.final_artifact_chain_load(args)
    captured = capsys.readouterr()
    assert "ArtifactChain" in captured.out

def test_final_closure_checks(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_checks(args)
    captured = capsys.readouterr()
    assert "ClosureChecks" in captured.out

def test_final_schema_lineage_safety_check(capsys):
    args = SimpleNamespace(write=False)
    cli.final_schema_lineage_safety_check(args)
    captured = capsys.readouterr()
    assert "Safety Rule" in captured.out

def test_build_freeze_seal(capsys):
    args = SimpleNamespace(write=False)
    cli.build_freeze_seal(args)
    captured = capsys.readouterr()
    assert "FreezeSeal" in captured.out

def test_engine_readiness_certificate(capsys):
    args = SimpleNamespace(write=False)
    cli.engine_readiness_certificate(args)
    captured = capsys.readouterr()
    assert "EngineCertificate" in captured.out

def test_phase126_kickoff_gate(capsys):
    args = SimpleNamespace(write=False)
    cli.phase126_kickoff_gate(args)
    captured = capsys.readouterr()
    assert "KickoffGate" in captured.out

def test_final_closure_safety_check(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_safety_check(args)
    captured = capsys.readouterr()
    assert "Safety:" in captured.out

def test_final_closure_context(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_context(args)
    captured = capsys.readouterr()
    assert "Context" in captured.out

def test_final_closure_review(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_review(args)
    captured = capsys.readouterr()
    assert "Review" in captured.out

def test_final_closure_summary(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_summary(args)
    captured = capsys.readouterr()
    assert "Store Summary" in captured.out

def test_final_closure_validate(capsys):
    args = SimpleNamespace(write=False)
    cli.final_closure_validate(args)
    captured = capsys.readouterr()
    assert "ValidationReport" in captured.out
