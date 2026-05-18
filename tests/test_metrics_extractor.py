import pytest
from usa_signal_bot.research_execution.metrics_extractor import extract_common_metrics

def test_extract_common_metrics_from_nested():
    payload = {
        "metrics": {
            "total_net_pnl_usd": 100.5,
            "custom_metric": 50,
            "max_drawdown_pct": "12.5"
        }
    }
    extracted = extract_common_metrics(payload)
    assert extracted["total_net_pnl_usd"] == 100.5
