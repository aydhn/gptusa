from usa_signal_bot.paper_observation.observation_models import ObservationScorecard, ObservationScoreStatus, ObservationRiskFlag
from usa_signal_bot.paper_observation.exit_decision_board import QuarantineExitDecisionBoard

def test_decision_board_clean():
    board = QuarantineExitDecisionBoard()
    sc = ObservationScorecard(
        scorecard_id="sc1", created_at_utc="2023", window_id="w1", candidate_id="c1",
        status=ObservationScoreStatus.PASS, score=100.0, session_score=100.0, checkpoint_score=100.0,
        telemetry_score=100.0, safety_score=100.0, notification_score=100.0, risk_flags=[],
        manual_review_required=False
    )
    decision = board.decide(sc, [])
    assert decision == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"

def test_decision_board_blocked():
    board = QuarantineExitDecisionBoard()
    sc = ObservationScorecard(
        scorecard_id="sc1", created_at_utc="2023", window_id="w1", candidate_id="c1",
        status=ObservationScoreStatus.FAIL, score=0.0, session_score=100.0, checkpoint_score=100.0,
        telemetry_score=100.0, safety_score=100.0, notification_score=100.0,
        risk_flags=[ObservationRiskFlag.REAL_ORDER_RISK],
        manual_review_required=True
    )
    decision = board.decide(sc, [])
    assert decision == "BLOCK_CANDIDATE"
