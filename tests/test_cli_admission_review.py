import subprocess

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def test_cli_admission_review_commands():
    # Only run info to check if CLI parsing doesn't crash
    res = run_cmd(["python", "-m", "usa_signal_bot", "admission-review-info"])
    assert res.returncode == 0
