import os
from pathlib import Path

def update_quality():
    path = Path("usa_signal_bot/quality/data_quality_evaluator.py")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("class DataQualityEvaluator:\n    pass\n")

    content = path.read_text()
    if "final_dry_admission_gate_score" not in content:
        to_add = """
    def get_dry_admission_gate_scores(self, payload: dict) -> dict:
        return {
            "final_dry_admission_gate_score": 100 if payload.get("dry_admission_gate_passed") else 0,
            "shadow_launch_replay_score": 100 if payload.get("shadow_replay_passed") else 0,
            "board_evidence_freeze_score": 100 if payload.get("board_evidence_freeze_valid") else 0,
            "dry_admission_assertion_score": 100 if payload.get("assertions_passed") else 0,
            "dry_admission_non_execution_compliance_score": 100 if payload.get("all_writes_blocked") else 0
        }
"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('class DataQualityEvaluator:'):
                lines.insert(i+1, to_add)
                break
        content = '\n'.join(lines)
        path.write_text(content)

def update_observability():
    path = Path("usa_signal_bot/observability/metrics_collector.py")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("class MetricsCollector:\n    def __init__(self):\n        self.metrics = {}\n")

    content = path.read_text()
    if "latest_dry_admission_gate_count" not in content:
        to_add = """
    def update_dry_admission_gate_metrics(self, payload: dict):
        self.metrics["latest_dry_admission_gate_count"] = self.metrics.get("latest_dry_admission_gate_count", 0) + 1
        if payload.get("blocked", False):
            self.metrics["latest_dry_admission_gate_blocked_count"] = self.metrics.get("latest_dry_admission_gate_blocked_count", 0) + 1
        self.metrics["latest_shadow_replay_count"] = self.metrics.get("latest_shadow_replay_count", 0) + 1
        self.metrics["latest_shadow_replay_allowed_attempt_count"] = payload.get("allowed_attempt_count", 0)
        self.metrics["latest_board_evidence_freeze_count"] = self.metrics.get("latest_board_evidence_freeze_count", 0) + 1
        self.metrics["latest_board_evidence_freeze_failed_count"] = payload.get("freeze_failed_count", 0)
        self.metrics["latest_dry_admission_rule_failed_count"] = payload.get("rule_failed_count", 0)
        self.metrics["latest_dry_admission_assertion_failed_count"] = payload.get("assertion_failed_count", 0)
        self.metrics["latest_dry_admission_safety_flag_count"] = payload.get("safety_flag_count", 0)
        self.metrics["dry_admission_gate_warning_count"] = payload.get("warning_count", 0)
"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('class MetricsCollector:'):
                lines.insert(i+1, to_add)
                break
        content = '\n'.join(lines)
        path.write_text(content)

update_quality()
update_observability()
