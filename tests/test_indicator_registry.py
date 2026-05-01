from usa_signal_bot.core.enums import IndicatorOutputType
import pytest
from usa_signal_bot.features.indicator_registry import IndicatorRegistry, create_default_indicator_registry
from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.core.enums import IndicatorCategory
from usa_signal_bot.core.exceptions import IndicatorRegistrationError
from usa_signal_bot.features.indicator_params import IndicatorParameterSchema

class DummyIndicator(Indicator):
    @property
    def metadata(self) -> IndicatorMetadata:
        return IndicatorMetadata(
            name="dummy",
            version="1.0",
            category=IndicatorCategory.CUSTOM,
            description="Dummy",
            required_columns=["close"],
            min_bars=1,
            output_type=IndicatorOutputType.SERIES,
            default_params={},
            produces=["dummy"]
        )
    @property
    def parameter_schema(self) -> IndicatorParameterSchema:
        return IndicatorParameterSchema("dummy", [])
    def compute(self, df, params=None):
        return df

def test_registry_registration():
    reg = IndicatorRegistry()
    ind = DummyIndicator()
    reg.register(ind)
    assert reg.has("dummy")
    assert reg.get("dummy") == ind

def test_registry_duplicate_registration():
    reg = IndicatorRegistry()
    ind = DummyIndicator()
    reg.register(ind)
    with pytest.raises(IndicatorRegistrationError):
        reg.register(ind)

def test_default_registry():
    reg = create_default_indicator_registry()
    assert reg.has("close_sma")
    assert reg.has("sma")
    assert reg.has("ema")
    assert reg.has("macd")

def test_list_by_category():
    reg = create_default_indicator_registry()
    trend_inds = reg.list_by_category(IndicatorCategory.TREND)
    names = [i.metadata.name for i in trend_inds]
    assert "sma" in names
    assert "ema" in names
    assert "macd" in names

def test_validate_all():
    reg = create_default_indicator_registry()
    reg.validate_all() # Should not raise

def test_momentum_in_registry():
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    reg = create_default_indicator_registry()
    assert reg.has("rsi")
    assert reg.has("stochastic")
    assert reg.has("roc")
