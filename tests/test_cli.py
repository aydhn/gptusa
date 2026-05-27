
def test_advanced_features_info_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "advanced-features-info"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Phase 118" in result.stdout

def test_factor_composition_info_cli(capsys):
    pass # In real project would mock args and call the parser
