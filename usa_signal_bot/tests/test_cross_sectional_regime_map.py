import pytest
from usa_signal_bot.regime_map.cross_sectional_regime_map import CrossSectionalRegimeMapBuilder
from usa_signal_bot.core.enums import CrossSectionalRegime

def test_cross_sectional_map_insufficient():
    builder = CrossSectionalRegimeMapBuilder()
    m = builder.build_map([])
    assert m.cross_sectional_regime == CrossSectionalRegime.INSUFFICIENT_DATA
    assert m.symbol_count == 0
