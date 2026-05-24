from typing import Any

class MetricsCollector:

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

    def __init__(self):
        self.metrics = {
            "latest_advanced_transition_context_count": 0,
            "latest_advanced_transition_ready_count": 0,
            "latest_handoff_freeze_ingestion_valid_count": 0,
            "latest_runtime_boundary_manifest_count": 0,
            "latest_blocked_runtime_capability_count": 0,
            "latest_module_inventory_record_count": 0,
            "latest_phase101_config_issue_count": 0,
            "latest_phase101_validation_issue_count": 0,
            "latest_phase101_execution_violation_count": 0,

            "latest_board_dossier_count": 0,
            "latest_board_dossier_blocked_count": 0,
            "latest_acceptance_board_seal_count": 0,
            "latest_acceptance_board_seal_failed_count": 0,
            "latest_shadow_launch_blocker_event_count": 0,
            "latest_shadow_launch_attempt_blocked_count": 0,
            "latest_shadow_launch_attempt_not_blocked_count": 0,
            "latest_shadow_launch_allowed_violation_count": 0,
            "latest_board_dossier_safety_flag_count": 0,
            "board_dossier_warning_count": 0
        }

    def collect_board_dossier_metrics(self, review: Any) -> None:
        self.metrics["latest_board_dossier_count"] = len(review.dossiers)
        self.metrics["latest_board_dossier_blocked_count"] = sum(1 for d in review.dossiers if d.status.name == "BLOCKED")
        self.metrics["latest_acceptance_board_seal_count"] = len(review.acceptance_board_seals)
        self.metrics["latest_shadow_launch_blocker_event_count"] = len(review.shadow_launch_blocker_events)
        self.metrics["latest_shadow_launch_attempt_blocked_count"] = sum(1 for e in review.shadow_launch_blocker_events if e.blocked)
        self.metrics["latest_shadow_launch_attempt_not_blocked_count"] = sum(1 for e in review.shadow_launch_blocker_events if not e.blocked)

    def update_advanced_transition_metrics(self, payload: dict):
        self.metrics["latest_advanced_transition_context_count"] = self.metrics.get("latest_advanced_transition_context_count", 0) + 1
        self.metrics["latest_advanced_transition_ready_count"] = self.metrics.get("latest_advanced_transition_ready_count", 0) + payload.get("ready_count", 0)
        self.metrics["latest_handoff_freeze_ingestion_valid_count"] = self.metrics.get("latest_handoff_freeze_ingestion_valid_count", 0) + payload.get("valid_handoff_count", 0)
        self.metrics["latest_runtime_boundary_manifest_count"] = self.metrics.get("latest_runtime_boundary_manifest_count", 0) + 1
        self.metrics["latest_blocked_runtime_capability_count"] = self.metrics.get("latest_blocked_runtime_capability_count", 0) + payload.get("blocked_capability_count", 0)
        self.metrics["latest_module_inventory_record_count"] = self.metrics.get("latest_module_inventory_record_count", 0) + payload.get("module_count", 0)
        self.metrics["latest_phase101_config_issue_count"] = self.metrics.get("latest_phase101_config_issue_count", 0) + payload.get("config_issue_count", 0)
        self.metrics["latest_phase101_validation_issue_count"] = self.metrics.get("latest_phase101_validation_issue_count", 0) + payload.get("validation_issue_count", 0)
        self.metrics["latest_phase101_execution_violation_count"] = self.metrics.get("latest_phase101_execution_violation_count", 0) + payload.get("execution_violation_count", 0)
