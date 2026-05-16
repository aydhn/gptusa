import sys
from io import StringIO
import pytest
from usa_signal_bot.app.cli import handle_portfolio_construction_info, handle_sector_cluster_write_example

class MockContext:
    pass

def test_portfolio_info():
    ctx = MockContext()
    saved_stdout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out
        assert handle_portfolio_construction_info(ctx) == 0
        assert "Portfolio Construction" in out.getvalue()
    finally:
        sys.stdout = saved_stdout

def test_sector_example(tmp_path):
    import os
    os.makedirs("config/portfolio", exist_ok=True)
    ctx = MockContext()
    assert handle_sector_cluster_write_example(ctx) == 0
