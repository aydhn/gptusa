from dataclasses import dataclass, asdict
from typing import List, Any, Dict, Optional

from usa_signal_bot.core.enums import IndicatorCategory, IndicatorOutputType
from usa_signal_bot.core.exceptions import ValidationError

@dataclass
class IndicatorMetadata:
    name: str
    version: str
    category: IndicatorCategory
    output_type: IndicatorOutputType
    description: str
    required_columns: List[str]
    default_params: Dict[str, Any]
    min_bars: int
    produces: List[str]
    supports_timeframes: Optional[List[str]] = None

def validate_indicator_metadata(metadata: IndicatorMetadata) -> None:
    if not metadata.name:
        raise ValidationError("Indicator name cannot be empty")
    if not metadata.version:
        raise ValidationError("Indicator version cannot be empty")
    if metadata.min_bars <= 0:
        raise ValidationError("Indicator min_bars must be positive")
    if not metadata.required_columns:
        raise ValidationError("Indicator required_columns cannot be empty")
    if not metadata.produces:
        raise ValidationError("Indicator produces cannot be empty")

    if not isinstance(metadata.category, IndicatorCategory):
        try:
            IndicatorCategory(metadata.category)
        except ValueError:
            raise ValidationError(f"Invalid category: {metadata.category}")

    if not isinstance(metadata.output_type, IndicatorOutputType):
        try:
            IndicatorOutputType(metadata.output_type)
        except ValueError:
            raise ValidationError(f"Invalid output_type: {metadata.output_type}")

def indicator_metadata_to_dict(metadata: IndicatorMetadata) -> dict:
    d = asdict(metadata)
    d["category"] = metadata.category.value if hasattr(metadata.category, "value") else str(metadata.category)
    d["output_type"] = metadata.output_type.value if hasattr(metadata.output_type, "value") else str(metadata.output_type)
    return d

def metadata_summary_text(metadata: IndicatorMetadata) -> str:
    supports = ", ".join(metadata.supports_timeframes) if metadata.supports_timeframes else "All"
    return f"Indicator {metadata.name} (v{metadata.version}) - {metadata.category.value}\n" \
           f"Type: {metadata.output_type.value}, Min Bars: {metadata.min_bars}\n" \
           f"Requires: {', '.join(metadata.required_columns)}\n" \
           f"Produces: {', '.join(metadata.produces)}\n" \
           f"Supports Timeframes: {supports}\n" \
           f"Description: {metadata.description}"
