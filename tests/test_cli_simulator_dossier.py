import subprocess

def run_cmd(cmd):
    result = subprocess.run(f"python -m usa_signal_bot {cmd}", shell=True, capture_output=True, text=True)
    return result

def test_simulator_dossier_cli():
    assert run_cmd("simulator-dossier-info").returncode == 0
    assert run_cmd("simulator-dossier-ingest-gate").returncode == 0
    assert run_cmd("simulator-dossier-eligibility").returncode == 0
    assert run_cmd("simulator-dossier-evidence").returncode == 0
    assert run_cmd("simulator-dossier").returncode == 0
    assert run_cmd("simulator-acceptance-seal").returncode == 0
    assert run_cmd("simulator-acceptance-seal-validate").returncode == 0
    assert run_cmd("sandbox-runtime-admission-blocker-rules").returncode == 0
    assert run_cmd("sandbox-runtime-admission-blocker-evaluate --attempt-type start_paper_sandbox_runtime").returncode == 0
    assert run_cmd("sandbox-runtime-admission-attempt-simulate").returncode == 0
    assert run_cmd("sandbox-runtime-admission-blocker-analyze").returncode == 0
    assert run_cmd("simulator-dossier-continuity").returncode == 0
    assert run_cmd("simulator-dossier-safety-check").returncode == 0
    assert run_cmd("simulator-dossier-audit").returncode == 0
    assert run_cmd("simulator-dossier-review").returncode == 0
    assert run_cmd("simulator-dossier-summary").returncode == 0
    assert run_cmd("simulator-dossier-latest-review").returncode == 0
    assert run_cmd("simulator-dossier-validate").returncode == 0
    assert run_cmd("simulator-dossier-notification-preview").returncode == 0
    assert run_cmd("simulator-dossier-notification-dispatch-dry-run").returncode == 0
