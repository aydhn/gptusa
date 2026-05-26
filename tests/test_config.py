from usa_signal_bot.core.config_schema import Config
def test_config():
    c = Config()
    assert c.core_indicators.current_phase == 117
