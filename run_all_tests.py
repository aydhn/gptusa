import pytest
import sys
exit_code = pytest.main(["tests/"])
sys.exit(exit_code)
