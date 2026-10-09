"""Offline ML loop: purged/embargoed validation, leakage guards, model registry, promotion gate.

Activation is never automatic: promotion only makes a model ELIGIBLE and a named human must approve
it. Nothing here is connected to any trading path.
"""

from usa_signal_bot.ml_loop.cv import PurgedKFold, assert_no_leakage
from usa_signal_bot.ml_loop.leakage import LeakageReport, check_leakage
from usa_signal_bot.ml_loop.registry import ModelRecord, ModelRegistry, PromotionThresholds
from usa_signal_bot.ml_loop.training import TrainingResult, run_training

__all__ = [
    "LeakageReport",
    "ModelRecord",
    "ModelRegistry",
    "PromotionThresholds",
    "PurgedKFold",
    "TrainingResult",
    "assert_no_leakage",
    "check_leakage",
    "run_training",
]
