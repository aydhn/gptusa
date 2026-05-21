import os
from pathlib import Path

FILES = {}

FILES["tests/test_checkpoint_history.py"] = """\
from usa_signal_bot.paper_observation.checkpoint_history import (
    build_checkpoint_history_entry, build_checkpoint_history, checkpoint_history_status,
    checkpoint_history_warnings, checkpoint_history_summary, checkpoint_history_to_text
)
from usa_signal_bot.core.enums import CheckpointHistoryStatus

def test_checkpoint_history():
    c1 = {"checkpoint_id": "cp1", "status": "REVIEWED"}
    c2 = {"checkpoint_id": "cp2", "status": "WAITING_REVIEW"}

    entry = build_checkpoint_history_entry(c1)
    assert entry.checkpoint_id == "cp1"
    assert entry.allows_active_paper is False

    history = build_checkpoint_history([c1, c2])
    assert len(history) == 2

    assert checkpoint_history_status([]) == CheckpointHistoryStatus.EMPTY
    assert checkpoint_history_status(history) == CheckpointHistoryStatus.PARTIAL

    complete_history = build_checkpoint_history([c1, {"checkpoint_id": "cp3", "status": "APPROVED"}])
    assert checkpoint_history_status(complete_history) == CheckpointHistoryStatus.COMPLETE

    warnings = checkpoint_history_warnings(history)
    assert any("waiting for review" in w for w in warnings)

    summary = checkpoint_history_summary(history)
    assert summary["waiting_review_count"] == 1

    text = checkpoint_history_to_text(history)
    assert "PARTIAL" in text
"""

FILES["tests/test_checkpoint_timeline.py"] = """\
from usa_signal_bot.paper_observation.checkpoint_history import build_checkpoint_history
from usa_signal_bot.paper_observation.checkpoint_timeline import (
    sort_checkpoint_history, latest_checkpoint, checkpoint_timeline_has_stale_review,
    checkpoint_timeline_required_followups, checkpoint_timeline_summary, checkpoint_timeline_to_text
)

def test_checkpoint_timeline():
    history = build_checkpoint_history([
        {"checkpoint_id": "cp1", "status": "REVIEWED"},
        {"checkpoint_id": "cp2", "status": "WAITING_REVIEW"}
    ])

    # modify dates slightly
    history[0].created_at_utc = "2023-01-01T00:00:00Z"
    history[1].created_at_utc = "2023-01-02T00:00:00Z"

    sorted_h = sort_checkpoint_history(history)
    assert sorted_h[0].checkpoint_id == "cp1"

    latest = latest_checkpoint(history)
    assert latest is not None
    assert latest.checkpoint_id == "cp2"

    # Since dates are old, it should be stale
    assert checkpoint_timeline_has_stale_review(history) is True

    followups = checkpoint_timeline_required_followups(history)
    assert len(followups) > 0

    summary = checkpoint_timeline_summary(history)
    assert summary["is_stale"] is True

    text = checkpoint_timeline_to_text(history)
    assert "Yes" in text
"""

FILES["tests/test_telemetry_history.py"] = """\
from usa_signal_bot.paper_observation.telemetry_history import (
    aggregate_bridge_telemetry_history, count_telemetry_event_types,
    count_telemetry_safety_flags, telemetry_history_warnings, telemetry_history_to_text
)

def test_telemetry_history():
    events = [
        {"event_type": "PROPOSAL", "session_id": "s1"},
        {"event_type": "BLOCKED_OPERATION", "session_id": "s1", "safety_flags": ["REAL_ORDER_RISK"]}
    ]

    counts = count_telemetry_event_types(events)
    assert counts["PROPOSAL"] == 1

    flags = count_telemetry_safety_flags(events)
    assert flags["REAL_ORDER_RISK"] == 1

    warnings = telemetry_history_warnings(events)
    assert len(warnings) == 1

    summary = aggregate_bridge_telemetry_history(events)
    assert summary.event_count == 2
    assert summary.blocked_operation_count == 1

    text = telemetry_history_to_text(summary)
    assert "Events: 2" in text
"""

FILES["tests/test_proposal_history.py"] = """\
from usa_signal_bot.paper_observation.proposal_history import (
    aggregate_proposal_history, count_proposals_by_type, count_proposals_by_status,
    proposal_history_warnings, proposal_history_to_text
)

def test_proposal_history():
    sessions = [
        {"proposals": [{"type": "BUY", "status": "BLOCKED"}, {"type": "SELL", "status": "APPROVED"}]}
    ]

    counts_t = count_proposals_by_type(sessions)
    assert counts_t["BUY"] == 1

    counts_s = count_proposals_by_status(sessions)
    assert counts_s["BLOCKED"] == 1

    warnings = proposal_history_warnings(sessions)
    assert len(warnings) == 1

    agg = aggregate_proposal_history(sessions)
    assert agg["total_proposals"] == 2

    text = proposal_history_to_text(agg)
    assert "Total: 2" in text
"""

FILES["tests/test_risk_history.py"] = """\
from usa_signal_bot.paper_observation.risk_history import (
    aggregate_risk_outcome_history, risk_warning_ratio, risk_rejection_ratio,
    risk_history_flags, risk_history_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def test_risk_history():
    sessions = [
        {"proposals": [1, 2], "risk_warning_count": 1, "risk_rejected_count": 2, "real_order_risk_detected": True}
    ]

    w_ratio = risk_warning_ratio(sessions)
    assert w_ratio == 0.5

    r_ratio = risk_rejection_ratio(sessions)
    assert r_ratio == 1.0

    flags = risk_history_flags(sessions)
    assert ObservationRiskFlag.REAL_ORDER_RISK in flags
    assert ObservationRiskFlag.RISK_REJECTION_HIGH in flags

    agg = aggregate_risk_outcome_history(sessions)
    assert agg["session_count"] == 1

    text = risk_history_to_text(agg)
    assert "Rejection Ratio: 1.00" in text
"""

FILES["tests/test_blocked_operation_history.py"] = """\
from usa_signal_bot.paper_observation.blocked_operation_history import (
    aggregate_blocked_operation_history, blocked_operation_count,
    blocked_operations_by_type, blocked_operation_risk_flags, blocked_operation_history_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def test_blocked_operation_history():
    events = [
        {"event_type": "BLOCKED_OPERATION", "operation_type": "REAL_ORDER"},
        {"event_type": "BLOCKED_OPERATION", "operation_type": "CONFIG_PATCH"}
    ]

    assert blocked_operation_count(events) == 2

    by_type = blocked_operations_by_type(events)
    assert by_type["REAL_ORDER"] == 1

    flags = blocked_operation_risk_flags(events)
    assert ObservationRiskFlag.BLOCKED_OPERATION_HISTORY in flags
    assert ObservationRiskFlag.REAL_ORDER_RISK in flags
    assert ObservationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK in flags

    agg = aggregate_blocked_operation_history(events)
    assert agg["total_blocked"] == 2

    text = blocked_operation_history_to_text(agg)
    assert "Total Blocked: 2" in text
"""

FILES["tests/test_notification_safety_history.py"] = """\
from usa_signal_bot.paper_observation.notification_safety_history import (
    aggregate_notification_safety_history, notification_warning_count,
    detect_unsafe_notification_history, notification_safety_risk_flags, notification_safety_history_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def test_notification_safety_history():
    sessions = [
        {"notification_warning_count": 1, "notifications": [{"text": "Gerçek emir gönderildi."}]},
        {"telegram_real_send_detected": True}
    ]

    assert notification_warning_count(sessions) == 1

    unsafe = detect_unsafe_notification_history(sessions)
    assert len(unsafe) > 0
    assert any("gerçek emir" in u for u in unsafe)

    flags = notification_safety_risk_flags(sessions)
    assert ObservationRiskFlag.NOTIFICATION_UNSAFE in flags
    assert ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK in flags

    agg = aggregate_notification_safety_history(sessions)
    assert agg["warning_count"] == 1

    text = notification_safety_history_to_text(agg)
    assert "Warnings: 1" in text
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
