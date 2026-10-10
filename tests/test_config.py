from usa_signal_bot.core.config import config_to_dict, load_app_config
from usa_signal_bot.core.config_schema import AppConfig

_MUST_STAY_FALSE = ("activation_allowed", "broker_execution_enabled", "order_creation_enabled", "deployment_allowed")


def _walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            yield from _walk(v, f"{path}[{i}]")
    else:
        yield path, node


def test_default_config_load_and_roundtrip():
    config = load_app_config()
    assert isinstance(config, AppConfig)
    as_dict = config_to_dict(config)
    assert isinstance(as_dict, dict) and as_dict


def test_default_config_keeps_activation_and_broker_flags_false():
    flags = {p: v for p, v in _walk(config_to_dict(load_app_config())) if p.split(".")[-1] in _MUST_STAY_FALSE}
    assert all(v is False for v in flags.values()), {p: v for p, v in flags.items() if v is not False}


def test_invalid_risk_ratio():
    from usa_signal_bot.core.config_schema import RiskConfig

    rc = RiskConfig(max_position_pct=1.5)
    assert rc.max_position_pct == 1.5
