import pytest
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLFoundationIngestionResult,
    MLAssembledDatasetManifest,
    MLMatrixAssemblyResult,
    MLDatasetSourceReference,
    MLMatrixKind,
    MLAssemblyMode,
    MLSplitPolicy,
    MLSplitPolicyKind,
    MLSplitAssignment,
    MLLeakageAuditResult,
    MLDatasetQualityProfile,
    MLSplitQualityProfile,
    MLDatasetQualityKind,
    MLDatasetQualityStatus,
    MLDatasetAssemblyQuality
)
from usa_signal_bot.ml_research.dataset_assembly.dataset_assembly_readiness_gate import (
    build_dataset_assembly_readiness_gate,
    dataset_assembly_readiness_passed
)

def test_readiness_gate_passes_when_all_conditions_met():
    ingestion = MLFoundationIngestionResult(ingestion_id="i1", created_at_utc="now", source_path=None, source_review_id=None, source_context_id=None, available=True, final_closure_ingested=True, final_closure_artifacts_loaded=True, source_registry_built=True, feature_contract_built=True, target_contract_built=True, label_contract_built=True, dataset_contract_built=True, leakage_guard_built=True, non_activation_boundary_validated=True, governance_built=True, readiness_gate_built=True, readiness_gate_passed=True, ready_for_phase137=True, metadata_only=True, research_data_only=True, activation_allowed=False, strategy_activation_allowed=False, deployment_allowed=False, active_paper_enabled=False, broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False, html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False, daemon_started=False, scheduler_enabled=False, training_started=False, prediction_started=False, model_training_used=False, model_prediction_used=False, heavy_ml_dependency_used=False, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, investment_advice=False, network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False, broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False, valid_for_phase137=True)

    mat_res = MLMatrixAssemblyResult(result_id="m1", created_at_utc="now", matrix_kind=MLMatrixKind.FEATURE_MATRIX, assembly_mode=MLAssemblyMode.LOCAL_ARTIFACT, row_count=10, column_count=5, assembly_valid=True)

    manifest = MLAssembledDatasetManifest(manifest_id="mf1", created_at_utc="now", manifest_version="1", feature_matrix=mat_res, target_matrix=mat_res, label_matrix=mat_res, manifest_valid=True, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False)

    split_policy = MLSplitPolicy(policy_id="sp1", created_at_utc="now", policy_kind=MLSplitPolicyKind.SYMBOL_AWARE_TIME_SPLIT, policy_name="test")
    split_assignment = MLSplitAssignment(assignment_id="sa1", created_at_utc="now", policy_id="sp1", split_assignment_valid=True)
    leakage_audit = MLLeakageAuditResult(audit_id="la1", created_at_utc="now", leakage_audit_passed=True)

    dqp = MLDatasetQualityProfile(profile_id="qp1", created_at_utc="now", quality_kind=MLDatasetQualityKind.ROW_COUNT_QUALITY, status=MLDatasetQualityStatus.ACCEPTABLE, score=100.0)
    sqp = MLSplitQualityProfile(profile_id="sq1", created_at_utc="now", policy_id="sp1", status=MLDatasetQualityStatus.ACCEPTABLE, score=100.0)

    gate = build_dataset_assembly_readiness_gate(
        ingestion, manifest, split_policy, split_assignment, leakage_audit, [dqp], sqp
    )

    assert dataset_assembly_readiness_passed(gate) is True
    assert gate.ready_for_phase138 is True
