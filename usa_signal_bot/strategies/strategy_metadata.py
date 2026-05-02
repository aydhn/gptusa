from dataclasses import dataclass, field
from typing import Optional, List
from usa_signal_bot.core.enums import StrategyCategory, StrategyStatus, SignalAction
from usa_signal_bot.core.exceptions import StrategyMetadataError

@dataclass
class StrategyMetadata:
    name: str
    version: str
    category: StrategyCategory
    status: StrategyStatus
    description: str
    required_features: List[str]
    produces_actions: List[SignalAction]
    optional_features: List[str] = field(default_factory=list)
    supported_timeframes: Optional[List[str]] = None
    experimental: bool = True
    notes: List[str] = field(default_factory=list)

def validate_strategy_metadata(metadata: StrategyMetadata) -> None:
    if not metadata.name:
        raise StrategyMetadataError("Strategy name cannot be empty")
    if not metadata.version:
        raise StrategyMetadataError("Strategy version cannot be empty")
    if not isinstance(metadata.category, StrategyCategory):
        try:
            metadata.category = StrategyCategory(metadata.category)
        except ValueError:
            raise StrategyMetadataError(f"Invalid category: {metadata.category}")
    if not isinstance(metadata.status, StrategyStatus):
        try:
            metadata.status = StrategyStatus(metadata.status)
        except ValueError:
            raise StrategyMetadataError(f"Invalid status: {metadata.status}")
    if not isinstance(metadata.required_features, list):
        raise StrategyMetadataError("required_features must be a list")
    if not metadata.produces_actions:
        raise StrategyMetadataError("produces_actions cannot be empty")

    has_execution_actions = any(a in [SignalAction.LONG, SignalAction.SHORT] for a in metadata.produces_actions)
    if has_execution_actions:
        has_warning = any("execution" in str(n).lower() and "not" in str(n).lower() for n in metadata.notes)
        if not has_warning:
            metadata.notes.append("WARNING: This strategy produces LONG/SHORT candidates. These are NOT execution orders.")

def strategy_metadata_to_dict(metadata: StrategyMetadata) -> dict:
    return {
        "name": metadata.name,
        "version": metadata.version,
        "category": metadata.category.value if isinstance(metadata.category, StrategyCategory) else metadata.category,
        "status": metadata.status.value if isinstance(metadata.status, StrategyStatus) else metadata.status,
        "description": metadata.description,
        "required_features": metadata.required_features,
        "optional_features": metadata.optional_features,
        "supported_timeframes": metadata.supported_timeframes,
        "produces_actions": [a.value if isinstance(a, SignalAction) else a for a in metadata.produces_actions],
        "experimental": metadata.experimental,
        "notes": metadata.notes
    }

def strategy_metadata_summary_text(metadata: StrategyMetadata) -> str:
    lines = [
        f"Strategy: {metadata.name} (v{metadata.version})",
        f"Category: {metadata.category.value if isinstance(metadata.category, StrategyCategory) else metadata.category}",
        f"Status: {metadata.status.value if isinstance(metadata.status, StrategyStatus) else metadata.status}",
        f"Experimental: {metadata.experimental}",
        f"Description: {metadata.description}",
        f"Produces: {[a.value if isinstance(a, SignalAction) else a for a in metadata.produces_actions]}",
        f"Required Features: {metadata.required_features}"
    ]
    if metadata.supported_timeframes:
        lines.append(f"Supported Timeframes: {metadata.supported_timeframes}")
    if metadata.notes:
        lines.append("Notes:")
        for note in metadata.notes:
            lines.append(f"  - {note}")
    return "\n".join(lines)
