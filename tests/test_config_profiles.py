from usa_signal_bot.release.config_profiles import default_config_profiles, write_default_config_profiles, validate_config_profile
from pathlib import Path

def test_config_profiles(tmp_path):
    paths = write_default_config_profiles(tmp_path)
    assert len(paths) == 4

    profs = default_config_profiles(tmp_path)
    # validate paper_dry_run which we wrote
    profs[1].config_path = str(tmp_path / profs[1].config_path)
    res = validate_config_profile(profs[1])
    assert res.status.value == "PASSED"
