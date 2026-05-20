from usa_signal_bot.paper_observation.observation_models import ObservationScorecard, QuarantineExitDecision, ObservationRiskFlag
from typing import Any

class QuarantineExitDecisionBoard:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def decide(self, scorecard: ObservationScorecard, gates: list[dict[str, Any]]) -> QuarantineExitDecision:
        if ObservationRiskFlag.REAL_ORDER_RISK in scorecard.risk_flags or ObservationRiskFlag.PAPER_STATE_MUTATION_RISK in scorecard.risk_flags:
            return QuarantineExitDecision.BLOCK_CANDIDATE
        if ObservationRiskFlag.CHECKPOINT_MISSING in scorecard.risk_flags or ObservationRiskFlag.CHECKPOINT_STALE in scorecard.risk_flags:
            return QuarantineExitDecision.REQUEST_MANUAL_REVIEW
        if ObservationRiskFlag.INSUFFICIENT_DRY_RUN_SESSIONS in scorecard.risk_flags:
            return QuarantineExitDecision.REQUEST_MORE_DRY_RUN_OBSERVATION

        # If clean:
        if len(scorecard.risk_flags) == 0 and scorecard.status == "PASS":
            return QuarantineExitDecision.ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING

        return QuarantineExitDecision.KEEP_IN_QUARANTINE
