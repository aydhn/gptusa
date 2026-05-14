import subprocess
import pytest

def test_cli_transaction_cost_info():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "transaction-cost-info"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Transaction Cost Module" in res.stdout

def test_cli_fee_schedule():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "fee-schedule"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Fee Schedule Proxy" in res.stdout

def test_cli_commission_estimate():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "commission-estimate", "--side", "sell", "--quantity", "10", "--notional", "1000"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Fee Proxy Estimate" in res.stdout

def test_cli_market_impact():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "market-impact", "--symbol", "SPY", "--side", "buy", "--notional", "1000", "--adv", "10000000"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Market Impact Estimate" in res.stdout
