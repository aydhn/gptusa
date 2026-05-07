import pytest

# Note: cli tests are often end-to-end integration tests that take time
# Here we just put a placeholder for paper tests since the others mock sys.argv

def test_paper_cli_import():
    import usa_signal_bot.app.cli as cli
    assert hasattr(cli, "cmd_paper_info")
    assert hasattr(cli, "cmd_paper_account_create")
