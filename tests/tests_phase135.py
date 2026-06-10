import os

tests_dir = "tests"
fixtures_dir = "tests/fixtures/regime_final_closure"
os.makedirs(fixtures_dir, exist_ok=True)

with open(f"{fixtures_dir}/sample_research_freeze_review.json", "w") as f:
    f.write('{}')

with open(f"{tests_dir}/test_phase135_models.py", "w") as f:
    f.write("""def test_models_import():
    import usa_signal_bot.regime_classification.final_closure.phase135_models
    assert True
""")

with open(f"{tests_dir}/test_cli_phase135.py", "w") as f:
    f.write("""def test_cli_import():
    from usa_signal_bot.regime_classification.final_closure import setup_phase135_cli
    assert True
""")
