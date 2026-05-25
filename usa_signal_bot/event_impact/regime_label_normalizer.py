
from typing import Optional
from usa_signal_bot.core.enums import MacroRegimeMetadataLabel

def normalize_regime_label(value: Optional[str]) -> MacroRegimeMetadataLabel:
    if not value: return MacroRegimeMetadataLabel.UNKNOWN_CONTEXT
    v = value.upper()
    if "RATE" in v and "RIS" in v: return MacroRegimeMetadataLabel.RATE_RISING_CONTEXT
    if "RATE" in v and "FALL" in v: return MacroRegimeMetadataLabel.RATE_FALLING_CONTEXT
    return MacroRegimeMetadataLabel.UNKNOWN_CONTEXT

def regime_label_to_human_text(label: MacroRegimeMetadataLabel) -> str:
    return label.value.replace("_", " ").title()

def regime_label_is_safe(label: MacroRegimeMetadataLabel) -> bool:
    return "CONTEXT" in label.value

def regime_label_normalizer_to_text(label: MacroRegimeMetadataLabel) -> str:
    return label.value
