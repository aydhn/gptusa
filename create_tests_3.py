import os
from pathlib import Path

FILES = {}

FILES["tests/test_observation_scoring.py"] = """\
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry, ObservationScoreStatus, ObservationRiskFlag
from usa_signal_bot.paper_observation.observation_scoring import build_observation_scorecard, observation_scorecard_to_text
import datetime

def test_observation_scoring():
    window = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
    telemetry = ObservationTelemetrySummary("t1", "2023", "w1", "c1", 10, 3, 3, 0, 0, 0, 0, 0)
    cp = CheckpointHistoryEntry("h1", datetime.datetime.now(datetime.timezone.utc).isoformat(), "cp1", "s1", "c1", "t1", "REVIEWED", None, None)

    sc = build_observation_scorecard(window, telemetry, [cp], [])
    assert sc.status == ObservationScoreStatus.PASS
    assert sc.score == 100.0

    # Missing session
    window.observed_session_count = 1
    sc2 = build_observation_scorecard(window, telemetry, [cp], [])
    assert sc2.status == ObservationScoreStatus.PASS
    assert sc2.score == 80.0
    assert ObservationRiskFlag.INSUFFICIENT_DRY_RUN_SESSIONS in sc2.risk_flags

    # Blocked operation (safety risk)
    telemetry.blocked_operation_count = 1
    sc3 = build_observation_scorecard(window, telemetry, [cp], [{"real_order_risk_detected": True}])
    assert sc3.status == ObservationScoreStatus.BLOCKED
    assert ObservationRiskFlag.REAL_ORDER_RISK in sc3.risk_flags

    text = observation_scorecard_to_text(sc)
    assert "100.0" in text
"""

FILES["tests/test_exit_gates.py"] = """\
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry
from usa_signal_bot.paper_observation.exit_gates import default_quarantine_exit_gates, exit_gates_to_text
import datetime

def test_exit_gates():
    window = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
    telemetry = ObservationTelemetrySummary("t1", "2023", "w1", "c1", 10, 3, 3, 0, 0, 0, 0, 0)
    cp = CheckpointHistoryEntry("h1", datetime.datetime.now(datetime.timezone.utc).isoformat(), "cp1", "s1", "c1", "t1", "REVIEWED", None, None)

    gates = default_quarantine_exit_gates(window, telemetry, [cp], [])
    assert len(gates) == 4
    assert all(g["passed"] for g in gates)

    text = exit_gates_to_text(gates)
    assert "Quarantine Exit Gates" in text
    assert "PASS" in text
"""

FILES["tests/test_exit_audit.py"] = """\
from usa_signal_bot.paper_observation.observation_models import QuarantineExitReview, QuarantineExitDecision
from usa_signal_bot.paper_observation.exit_audit import create_observation_audit_entry, audit_entry_from_exit_review, append_observation_audit_entry, observation_audit_summary, observation_audit_to_text

def test_exit_audit():
    entry = create_observation_audit_entry("Entity", "id1", "ACTION", "Rationale")
    assert entry.entity_id == "id1"

    rev = QuarantineExitReview("r1", "2023", "w1", "c1", "t1", QuarantineExitDecision.KEEP_IN_QUARANTINE, None, None, [], [], "Rationale", [], False)
    audit = audit_entry_from_exit_review(rev)
    assert audit.action == "QUARANTINE_EXIT_DECISION"
    assert audit.decision == "KEEP_IN_QUARANTINE"

    entries = append_observation_audit_entry([entry], audit)
    assert len(entries) == 2

    summ = observation_audit_summary(entries)
    assert summ["total_entries"] == 2

    text = observation_audit_to_text(entries)
    assert "Total Entries: 2" in text
"""

FILES["tests/test_observation_report.py"] = """\
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationTelemetrySummary, CheckpointHistoryEntry
from usa_signal_bot.paper_observation.observation_report import build_quarantine_exit_review, build_observation_review, observation_review_summary, observation_limitations_text, observation_review_to_text
import datetime

def test_observation_report():
    window = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
    telemetry = ObservationTelemetrySummary("t1", "2023", "w1", "c1", 10, 3, 3, 0, 0, 0, 0, 0)
    cp = CheckpointHistoryEntry("h1", datetime.datetime.now(datetime.timezone.utc).isoformat(), "cp1", "s1", "c1", "t1", "REVIEWED", None, None)

    exit_rev = build_quarantine_exit_review(window, telemetry, [cp])
    assert exit_rev.decision == "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING"

    obs_rev = build_observation_review(window, None, None)
    assert len(obs_rev.exit_reviews) == 1

    summ = observation_review_summary(obs_rev)
    assert "exit_decision" in summ

    lim = observation_limitations_text()
    assert "NOT investment advice" in lim

    text = observation_review_to_text(obs_rev)
    assert "Observation Review" in text
"""

FILES["tests/test_observation_store.py"] = """\
from usa_signal_bot.paper_observation.observation_store import (
    write_observation_window_json, observation_store_summary, read_observation_review_json,
    write_observation_review_json, get_latest_observation_review,
    observation_windows_dir, observation_reviews_dir, observation_store_dir
)
from usa_signal_bot.paper_observation.observation_models import ObservationWindow, ObservationReview
import tempfile
from pathlib import Path

def test_observation_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        w = ObservationWindow("w1", "2023", "c1", "t1", "PLANNED", "FULL_SUPERVISED_OBSERVATION", None, None, 3, 3, [], [], 0, 0, False)
        w_path = observation_windows_dir(root) / "w1.json"
        write_observation_window_json(w_path, w)
        assert w_path.exists()

        rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [w], [], [], [], [], [], {})
        r_path = observation_reviews_dir(root) / "r1.json"
        write_observation_review_json(r_path, rev)
        assert r_path.exists()

        loaded = read_observation_review_json(r_path)
        assert loaded["review_id"] == "r1"

        latest = get_latest_observation_review(root)
        assert latest == r_path

        summ = observation_store_summary(root)
        assert summ["windows"] == 1
        assert summ["reviews"] == 1
"""

FILES["tests/test_observation_reporting.py"] = """\
from usa_signal_bot.paper_observation.observation_reporting import observation_limitations_text, observation_review_to_text
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_observation_reporting():
    assert "NOT investment advice" in observation_limitations_text()

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    text = observation_review_to_text(rev)
    assert "Observation Review r1" in text
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
