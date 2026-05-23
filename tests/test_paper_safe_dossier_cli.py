import subprocess
import sys

def run_cmd(*args):
    return subprocess.run([sys.executable, "-m", "usa_signal_bot"] + list(args), capture_output=True, text=True)

def test_paper_safe_dossier_cli():
    r = run_cmd("paper-safe-dossier-info")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-ingest-gate")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-eligibility")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-evidence")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier")
    assert r.returncode == 0

    r = run_cmd("non-execution-seal")
    assert r.returncode == 0

    r = run_cmd("non-execution-seal-validate")
    assert r.returncode == 0

    r = run_cmd("pre-paper-runtime-map")
    assert r.returncode == 0

    r = run_cmd("runtime-route-map")
    assert r.returncode == 0

    r = run_cmd("runtime-map-validate")
    assert r.returncode == 0

    r = run_cmd("runtime-non-execution-assertions")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-continuity")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-safety-check")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-audit")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-review")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-summary")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-latest-review")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-validate")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-notification-preview")
    assert r.returncode == 0

    r = run_cmd("paper-safe-dossier-notification-dispatch-dry-run")
    assert r.returncode == 0
