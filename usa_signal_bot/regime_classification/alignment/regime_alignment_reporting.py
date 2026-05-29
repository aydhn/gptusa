from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    MarketBehaviorIngestionResult, FrozenFactorAlignmentReference, RegimeAwareAlignmentSpec,
    MarketBehaviorOverlaySpec, MarketBehaviorOverlayResult, RegimeContextCompatibilityResult,
    AlignmentDiagnosticsProfile, RegimeAlignmentReadinessGate, RegimeAlignmentContext,
    RegimeAlignmentFullReview
)

def market_behavior_ingestion_result_to_text(item: MarketBehaviorIngestionResult) -> str:
    return f"Ingestion {item.ingestion_id}"

def frozen_factor_alignment_reference_to_text(item: FrozenFactorAlignmentReference) -> str:
    return f"Ref {item.reference_id}"

def regime_aware_alignment_spec_to_text(item: RegimeAwareAlignmentSpec) -> str:
    return f"Align Spec {item.spec_id}"

def market_behavior_overlay_spec_to_text(item: MarketBehaviorOverlaySpec) -> str:
    return f"Overlay Spec {item.spec_id}"

def market_behavior_overlay_result_to_text(item: MarketBehaviorOverlayResult) -> str:
    return f"Overlay {item.overlay_id}"

def regime_context_compatibility_result_to_text(item: RegimeContextCompatibilityResult) -> str:
    return f"Compat {item.compatibility_id}"

def alignment_diagnostics_profile_to_text(item: AlignmentDiagnosticsProfile) -> str:
    return f"Diag {item.diagnostics_id}"

def regime_alignment_readiness_gate_to_text(item: RegimeAlignmentReadinessGate, limit: int = 300) -> str:
    return f"Gate Passed: {item.ready_for_phase132}"

def regime_alignment_context_to_text(item: RegimeAlignmentContext, limit: int = 300) -> str:
    return f"Context {item.context_id}"

def regime_alignment_full_review_to_text(item: RegimeAlignmentFullReview, limit: int = 300) -> str:
    return f"Review {item.review_id}"

def regime_alignment_store_summary_to_text(summary: dict[str, Any]) -> str:
    return str(summary)

def regime_alignment_limitations_text() -> str:
    return "Phase 131 limitations: no active trading, no execution."
