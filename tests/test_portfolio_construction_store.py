import pytest
from pathlib import Path
from usa_signal_bot.portfolio.construction.portfolio_construction_store import (
    portfolio_construction_store_dir,
    write_portfolio_construction_policy_json
)
from usa_signal_bot.portfolio.construction.portfolio_construction_policy import build_default_portfolio_construction_policy

def test_store_directory(tmp_path):
    d = portfolio_construction_store_dir(tmp_path)
    assert d.exists()
    assert d.name == "construction"

def test_write_policy(tmp_path):
    d = portfolio_construction_store_dir(tmp_path)
    policy = build_default_portfolio_construction_policy()
    p_path = d / "policy.json"
    write_portfolio_construction_policy_json(p_path, policy)

    assert p_path.exists()
