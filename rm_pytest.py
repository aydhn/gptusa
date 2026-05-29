import os
import glob

# Remove 'import pytest' from our newly created test files since the test runner doesn't have it installed
files = glob.glob("tests/test_*130*.py") + \
        glob.glob("tests/test_behavior*.py") + \
        glob.glob("tests/test_market_behavior*.py") + \
        glob.glob("tests/test_regime_behavior*.py") + \
        glob.glob("tests/test_diagnostics_inter*.py") + \
        glob.glob("tests/test_cross_symb*.py") + \
        glob.glob("tests/test_regime_transition_ingestion.py") + \
        glob.glob("tests/test_diagnostics_artifact_loader.py")

for f in files:
    with open(f, "r") as file:
        content = file.read()
    content = content.replace("import pytest\n", "")
    with open(f, "w") as file:
        file.write(content)
