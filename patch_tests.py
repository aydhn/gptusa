from pathlib import Path

# Fix ConfigProfile validation
f_path = Path("usa_signal_bot/release/config_profiles.py")
content = f_path.read_text()
content = content.replace("path = Path(profile.config_path)", "path = Path('.') / profile.config_path")
f_path.write_text(content)

# Fix live execution language check (it was emitting a WARNING instead of an ERROR for language)
f_path = Path("usa_signal_bot/release/release_validation.py")
content = f_path.read_text()
content = content.replace('issues.append(ReleaseValidationIssue("WARNING", "language",', 'issues.append(ReleaseValidationIssue("ERROR", "language",')
f_path.write_text(content)

# Fix test config profiles config path lookup
f_path = Path("tests/test_config_profiles.py")
content = f_path.read_text()
content = content.replace('res = validate_config_profile(profs[1])', "profs[1].config_path = str(tmp_path / profs[1].config_path)\n    res = validate_config_profile(profs[1])")
f_path.write_text(content)
