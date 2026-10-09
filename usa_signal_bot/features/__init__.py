"""Indicator interface, parameter schema and metadata.

Boundary: concrete feature pipelines live in ``feature_engine``.
"""

from usa_signal_bot.features.indicator_interface import Indicator
from usa_signal_bot.features.indicator_metadata import IndicatorMetadata
from usa_signal_bot.features.indicator_params import (
    IndicatorParameterSchema,
    IndicatorParameterSpec,
)

__all__ = [
    "Indicator",
    "IndicatorMetadata",
    "IndicatorParameterSchema",
    "IndicatorParameterSpec",
]
