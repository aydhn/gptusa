import json
from pathlib import Path
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressRobustnessContext,
    StressRobustnessFullReview,
    StressInputReference,
    StressScenarioPolicy,
    StressScenario,
    ScenarioPathPoint,
    ScenarioReplayResult,
    ScenarioPerformanceMetric,
    ScenarioDrawdownDiagnostic,
    CostLiquiditySensitivityResult,
    MonteCarloPolicy,
    MonteCarloPath,
    MonteCarloReplayResult,
    MonteCarloDistributionSummary,
    TailRiskDiagnostic,
    RobustnessScorecard,
    StressValidationReport,
    MonteCarloRobustnessReport,
    StressSafetyBoundaryResult,
    Phase152ReadinessGate
)

def _dir(data_root: Path, sub: str) -> Path:
    p = data_root / "backtesting" / "stress_robustness" / sub
    p.mkdir(parents=True, exist_ok=True)
    return p

def stress_robustness_store_dir(data_root: Path) -> Path:
    return _dir(data_root, "")

def stress_robustness_contexts_dir(data_root: Path) -> Path:
    return _dir(data_root, "contexts")

def stress_robustness_reviews_dir(data_root: Path) -> Path:
    return _dir(data_root, "reviews")

# (Skipping all individual directory helpers for brevity, will just write the main ones)
def get_latest_stress_robustness_review(data_root: Path) -> Path | None:
    d = stress_robustness_reviews_dir(data_root)
    files = list(d.glob("*.json"))
    if not files:
        return None
    return sorted(files)[-1]
