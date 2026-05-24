from typing import List, Dict, Any
from usa_signal_bot.core.enums import AdvancedTransitionPhaseBand
from usa_signal_bot.advanced_transition.phase101_models import AdvancedPhaseRoadmapItem

def build_advanced_phase_roadmap() -> List[AdvancedPhaseRoadmapItem]:
    return [
        AdvancedPhaseRoadmapItem(
            phase_start=101, phase_end=105, band=AdvancedTransitionPhaseBand.POST_MVP_REOPENING,
            title="POST_MVP_REOPENING", objective="MVP sonrası functional reopening, core runtime consolidation.",
            allowed_scope=["metadata", "tests"], blocked_scope=["active_paper", "broker", "dashboard"],
            output_expectation=["Metadata reviews", "Transition context"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=106, phase_end=115, band=AdvancedTransitionPhaseBand.DATA_PROVIDER_EXPANSION,
            title="DATA_PROVIDER_EXPANSION", objective="scraping olmadan ücretsiz çoklu veri sağlayıcı, makro/haber takvimi, veri kalite katmanı.",
            allowed_scope=["free APIs"], blocked_scope=["scraping", "paid APIs"], output_expectation=["Data sources"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=116, phase_end=125, band=AdvancedTransitionPhaseBand.FEATURE_ENGINE_EXPANSION,
            title="FEATURE_ENGINE_EXPANSION", objective="gelişmiş indicator, feature ve factor engine.",
            allowed_scope=["indicators"], blocked_scope=[], output_expectation=["Features"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=126, phase_end=135, band=AdvancedTransitionPhaseBand.REGIME_AND_MARKET_BEHAVIOR,
            title="REGIME_AND_MARKET_BEHAVIOR", objective="rejim sınıflandırma, piyasa davranışı, volatilite ve korelasyon bağlamı.",
            allowed_scope=["math modelling"], blocked_scope=[], output_expectation=["Regime models"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=136, phase_end=145, band=AdvancedTransitionPhaseBand.ML_AND_MODEL_GOVERNANCE,
            title="ML_AND_MODEL_GOVERNANCE", objective="GPU uyumlu ML, ensemble, calibration, drift, explainability, governance.",
            allowed_scope=["local ML"], blocked_scope=["auto-apply"], output_expectation=["ML Governance"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=146, phase_end=152, band=AdvancedTransitionPhaseBand.BACKTEST_ROBUSTNESS,
            title="BACKTEST_ROBUSTNESS", objective="transaction cost, slippage, walk-forward, benchmark, stress, Monte Carlo.",
            allowed_scope=["local backtests"], blocked_scope=["live orders"], output_expectation=["Robustness metrics"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=153, phase_end=157, band=AdvancedTransitionPhaseBand.PORTFOLIO_AND_RISK,
            title="PORTFOLIO_AND_RISK", objective="portfolio construction, sizing, risk budgeting, optimization, risk reports.",
            allowed_scope=["portfolio models"], blocked_scope=["live routing"], output_expectation=["Risk reports"], metadata={}
        ),
        AdvancedPhaseRoadmapItem(
            phase_start=158, phase_end=160, band=AdvancedTransitionPhaseBand.FINAL_ADVANCED_INTEGRATION,
            title="FINAL_ADVANCED_INTEGRATION", objective="full-system integration, acceptance rehearsal, final advanced delivery.",
            allowed_scope=["dry rehearsals"], blocked_scope=["live execution"], output_expectation=["Final Delivery"], metadata={}
        )
    ]

def roadmap_item_for_phase(phase_number: int) -> AdvancedPhaseRoadmapItem | None:
    for item in build_advanced_phase_roadmap():
        if item.phase_start <= phase_number <= item.phase_end:
            return item
    return None

def advanced_phase_band_for_phase(phase_number: int) -> AdvancedTransitionPhaseBand:
    item = roadmap_item_for_phase(phase_number)
    if item:
        return item.band
    return AdvancedTransitionPhaseBand.UNKNOWN

def validate_advanced_phase_roadmap(items: List[AdvancedPhaseRoadmapItem]) -> List[str]:
    errors = []
    if not items:
        errors.append("Roadmap is empty")
    return errors

def advanced_phase_roadmap_to_text(items: List[AdvancedPhaseRoadmapItem]) -> str:
    return "\n".join([f"{i.phase_start}-{i.phase_end}: {i.band.name}" for i in items])
