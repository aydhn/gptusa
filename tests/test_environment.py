import os
import pytest
from usa_signal_bot.core.environment import (
    get_env, require_env, get_bool_env, get_int_env, get_float_env, mask_secret
)
from usa_signal_bot.core.exceptions import EnvironmentConfigError

def test_get_env():
    os.environ["TEST_ENV"] = "test_val"
    assert get_env("TEST_ENV") == "test_val"
    assert get_env("NON_EXISTENT_ENV", "default") == "default"

def test_require_env():
    os.environ["REQ_ENV"] = "exists"
    assert require_env("REQ_ENV") == "exists"

    if "MISSING_REQ_ENV" in os.environ:
        del os.environ["MISSING_REQ_ENV"]

    with pytest.raises(EnvironmentConfigError):
        require_env("MISSING_REQ_ENV")

def test_get_bool_env():
    os.environ["BOOL_ENV_T"] = "true"
    os.environ["BOOL_ENV_F"] = "false"
    assert get_bool_env("BOOL_ENV_T") is True
    assert get_bool_env("BOOL_ENV_F") is False
    assert get_bool_env("MISSING_BOOL", default=True) is True

def test_get_int_env():
    os.environ["INT_ENV"] = "42"
    assert get_int_env("INT_ENV", 0) == 42

    os.environ["BAD_INT_ENV"] = "not_int"
    with pytest.raises(EnvironmentConfigError):
        get_int_env("BAD_INT_ENV", 0)

def test_get_float_env():
    os.environ["FLOAT_ENV"] = "3.14"
    assert get_float_env("FLOAT_ENV", 0.0) == 3.14

    os.environ["BAD_FLOAT_ENV"] = "not_float"
    with pytest.raises(EnvironmentConfigError):
        get_float_env("BAD_FLOAT_ENV", 0.0)

def test_mask_secret():
    assert mask_secret(None) == "<missing>"
    assert mask_secret("short") == "***"
    assert mask_secret("long_secret_value") == "lon***lue"
