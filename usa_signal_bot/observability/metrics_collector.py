from typing import Any

class MetricsCollector:

    def update_provider_abstraction_metrics(self, review: Any):
        self.metrics["latest_provider_abstraction_context_count"] = self.metrics.get("latest_provider_abstraction_context_count", 0) + 1
        if review.context.provider_abstraction_ready:
            self.metrics["latest_provider_abstraction_ready_count"] = self.metrics.get("latest_provider_abstraction_ready_count", 0) + 1
        self.metrics["latest_provider_registry_entry_count"] = len(review.registry_entries)
        self.metrics["latest_provider_adapter_skeleton_count"] = len(review.adapter_specs)
        self.metrics["latest_provider_capability_matrix_count"] = 1 if review.capability_matrix else 0
        self.metrics["latest_provider_unsafe_count"] = review.capability_matrix.unsafe_provider_count if review.capability_matrix else 0
        self.metrics["latest_provider_selector_request_count"] = 0
        self.metrics["latest_provider_network_fetch_violation_count"] = 1 if review.context.provider_network_fetch_enabled_now else 0
        self.metrics["latest_provider_scraping_violation_count"] = 1 if review.context.scraping_enabled else 0
        self.metrics["latest_phase106_execution_violation_count"] = 1 if review.context.activation_allowed else 0

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
            "board_dossier_warning_count": 0,

            "latest_runtime_registry_count": 0,
            "latest_runtime_registry_valid_count": 0,
            "latest_config_surface_record_count": 0,
            "latest_config_surface_conflict_count": 0,
            "latest_provider_capability_manifest_count": 0,
            "latest_provider_safety_manifest_count": 0,
            "latest_provider_safety_violation_count": 0,
            "latest_runtime_capability_policy_count": 0,
            "latest_phase102_execution_violation_count": 0,

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


    def update_phase102_advanced_runtime_metrics(self, payload: dict):
        self.metrics["latest_runtime_registry_count"] = self.metrics.get("latest_runtime_registry_count", 0) + 1
        self.metrics["latest_runtime_registry_valid_count"] = self.metrics.get("latest_runtime_registry_valid_count", 0) + payload.get("valid_registry_count", 0)
        self.metrics["latest_config_surface_record_count"] = self.metrics.get("latest_config_surface_record_count", 0) + payload.get("config_surface_record_count", 0)
        self.metrics["latest_config_surface_conflict_count"] = self.metrics.get("latest_config_surface_conflict_count", 0) + payload.get("config_surface_conflict_count", 0)
        self.metrics["latest_provider_capability_manifest_count"] = self.metrics.get("latest_provider_capability_manifest_count", 0) + payload.get("provider_capability_manifest_count", 0)
        self.metrics["latest_provider_safety_manifest_count"] = self.metrics.get("latest_provider_safety_manifest_count", 0) + payload.get("provider_safety_manifest_count", 0)
        self.metrics["latest_provider_safety_violation_count"] = self.metrics.get("latest_provider_safety_violation_count", 0) + payload.get("provider_safety_violation_count", 0)
        self.metrics["latest_runtime_capability_policy_count"] = self.metrics.get("latest_runtime_capability_policy_count", 0) + payload.get("runtime_capability_policy_count", 0)
        self.metrics["latest_phase102_execution_violation_count"] = self.metrics.get("latest_phase102_execution_violation_count", 0) + payload.get("execution_violation_count", 0)

# Phase 103 Metrics
# latest_runtime_service_graph_count
# latest_runtime_service_graph_valid_count
# latest_runtime_service_node_count
# latest_dependency_contract_count
# latest_dependency_cycle_count
# latest_dependency_contract_invalid_count
# latest_orchestration_plan_count
# latest_orchestration_dry_run_pass_count
# latest_orchestration_blocked_step_count
# latest_phase103_execution_violation_count

    def update_core_runtime_acceptance_metrics(self, payload: dict):
        self.metrics["latest_core_runtime_acceptance_report_count"] = self.metrics.get("latest_core_runtime_acceptance_report_count", 0) + 1
        self.metrics["latest_core_runtime_accepted_count"] = self.metrics.get("latest_core_runtime_accepted_count", 0) + payload.get("accepted_count", 0)
        self.metrics["latest_foundation_freeze_count"] = self.metrics.get("latest_foundation_freeze_count", 0) + 1
        self.metrics["latest_foundation_freeze_valid_count"] = self.metrics.get("latest_foundation_freeze_valid_count", 0) + payload.get("freeze_valid_count", 0)
        self.metrics["latest_provider_kickoff_gate_count"] = self.metrics.get("latest_provider_kickoff_gate_count", 0) + 1
        self.metrics["latest_provider_kickoff_gate_pass_count"] = self.metrics.get("latest_provider_kickoff_gate_pass_count", 0) + payload.get("gate_pass_count", 0)
        self.metrics["latest_phase106_ready_count"] = self.metrics.get("latest_phase106_ready_count", 0) + payload.get("ready_count", 0)
        self.metrics["latest_phase105_missing_evidence_count"] = self.metrics.get("latest_phase105_missing_evidence_count", 0) + payload.get("missing_evidence_count", 0)
        self.metrics["latest_phase105_stale_evidence_count"] = self.metrics.get("latest_phase105_stale_evidence_count", 0) + payload.get("stale_evidence_count", 0)
        self.metrics["latest_phase105_execution_violation_count"] = self.metrics.get("latest_phase105_execution_violation_count", 0) + payload.get("execution_violation_count", 0)


    # Phase 107
    latest_provider_runtime_context_count: int = 0
    latest_provider_runtime_ready_count: int = 0
    latest_provider_runtime_adapter_spec_count: int = 0
    latest_provider_contract_test_count: int = 0
    latest_provider_contract_test_failed_count: int = 0
    latest_provider_fetch_dry_run_count: int = 0
    latest_provider_fetch_dry_run_pass_count: int = 0
    latest_provider_cache_lookup_dry_run_count: int = 0
    latest_provider_network_violation_count: int = 0
    latest_phase107_execution_violation_count: int = 0


# Phase 108 metrics
def collect_phase108_metrics():
    return {
        "latest_provider_cache_context_count": 0,
        "latest_provider_cache_index_count": 0,
        "latest_provider_cache_record_count": 0,
        "latest_provider_cache_fresh_count": 0,
        "latest_provider_cache_stale_count": 0,
        "latest_provider_cache_missing_count": 0,
        "latest_fallback_dry_run_count": 0,
        "latest_fallback_exhausted_count": 0,
        "latest_source_comparison_count": 0,
        "latest_source_disagreement_high_count": 0,
        "latest_provider_cache_network_violation_count": 0,
        "latest_phase108_execution_violation_count": 0
    }

# Phase 110 metrics
latest_provider_orchestration_context_count: int = 0
latest_provider_route_plan_count: int = 0
latest_provider_route_result_count: int = 0
latest_source_blend_result_count: int = 0
latest_data_availability_report_count: int = 0
latest_data_availability_missing_count: int = 0
latest_data_availability_coverage_ratio: float = 0.0
latest_refresh_plan_count: int = 0
latest_refresh_required_count: int = 0
latest_refresh_high_priority_count: int = 0
latest_provider_orchestration_trade_language_violation_count: int = 0
latest_phase110_execution_violation_count: int = 0
