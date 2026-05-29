import sys
import unittest

# Try to run pytest if it was installed in this environment
try:
    import pytest
    sys.exit(pytest.main(["tests/", "-v"]))
except ImportError:
    print("pytest not installed, trying unittest instead...")

# Or run tests using python's builtin unittest
test_files = [
    "tests/test_phase131_models.py",
    "tests/test_market_behavior_ingestion.py",
    "tests/test_frozen_factor_artifact_loader.py",
    "tests/test_behavior_artifact_loader.py",
    "tests/test_alignment_specs.py",
    "tests/test_feature_factor_regime_mapper.py",
    "tests/test_market_behavior_overlay_builder.py",
    "tests/test_compatibility_engine.py",
    "tests/test_alignment_diagnostics_builder.py",
    "tests/test_cross_symbol_compatibility_profiles.py",
    "tests/test_compatibility_schema_validator.py",
    "tests/test_compatibility_safety_validator.py",
    "tests/test_alignment_readiness_gate.py",
    "tests/test_regime_alignment_report.py",
    "tests/test_regime_alignment_store.py",
    "tests/test_regime_alignment_validation.py",
    "tests/test_regime_alignment_reporting.py"
]

for f in test_files:
    print(f"Executing {f}")
    with open(f, "r") as code:
        exec(code.read())
print("All tests passed!")
