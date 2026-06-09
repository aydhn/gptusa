from typing import Any, Dict, List
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    AcceptanceScenario,
    AcceptanceScenarioMatrix,
    create_acceptance_scenario_id,
    create_acceptance_scenario_matrix_id,
    generate_timestamp,
    AcceptanceScenarioKind,
    AcceptanceAreaKind,
    AdvancedAcceptanceRiskFlag
)

def build_default_acceptance_scenarios() -> List[AcceptanceScenario]:
    base_forbidden = [
        "live_trading", "paper_state_mutation", "broker_execution", "real_order",
        "telegram_real_send", "deployment", "production_patch"
    ]

    scenarios = [
        {
            "kind": AcceptanceScenarioKind.FULL_CHAIN_REGRESSION,
            "area": AcceptanceAreaKind.CORE_RUNTIME,
            "name": "Full Chain Dry-Run Regression",
            "evidence": ["full_chain_dry_run_log.json"]
        },
        {
            "kind": AcceptanceScenarioKind.CONFIG_AND_RUNTIME_REGRESSION,
            "area": AcceptanceAreaKind.CONFIG,
            "name": "Config and Runtime Compatibility",
            "evidence": ["config_validation_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.DATA_PROVIDER_BOUNDARY_REGRESSION,
            "area": AcceptanceAreaKind.DATA_PROVIDER,
            "name": "Data Provider Safety Boundary",
            "evidence": ["data_provider_safety_log.json"]
        },
        {
            "kind": AcceptanceScenarioKind.FEATURE_ENGINE_REGRESSION,
            "area": AcceptanceAreaKind.FEATURE_ENGINE,
            "name": "Feature Engine Schema Validation",
            "evidence": ["feature_engine_schema_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.REGIME_ENGINE_REGRESSION,
            "area": AcceptanceAreaKind.REGIME_ENGINE,
            "name": "Regime Engine Dry-Run",
            "evidence": ["regime_engine_dry_run_log.json"]
        },
        {
            "kind": AcceptanceScenarioKind.ML_GOVERNANCE_REGRESSION,
            "area": AcceptanceAreaKind.ML_GOVERNANCE,
            "name": "ML Governance Safety Check",
            "evidence": ["ml_governance_safety_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.BACKTEST_CLOSURE_REGRESSION,
            "area": AcceptanceAreaKind.BACKTEST,
            "name": "Backtest Closure Consistency",
            "evidence": ["backtest_closure_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.PORTFOLIO_BAND_REGRESSION,
            "area": AcceptanceAreaKind.PORTFOLIO,
            "name": "Portfolio Band Governance",
            "evidence": ["portfolio_band_governance_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.INTEGRATION_BOUNDARY_REGRESSION,
            "area": AcceptanceAreaKind.INTEGRATION,
            "name": "Integration Boundary Safety",
            "evidence": ["integration_boundary_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.NOTIFICATION_DRY_RUN_REGRESSION,
            "area": AcceptanceAreaKind.NOTIFICATIONS,
            "name": "Notification Dry-Run",
            "evidence": ["notification_dry_run_log.json"]
        },
        {
            "kind": AcceptanceScenarioKind.QUALITY_OBSERVABILITY_REGRESSION,
            "area": AcceptanceAreaKind.QUALITY,
            "name": "Quality and Observability Metrics",
            "evidence": ["quality_observability_report.json"]
        },
        {
            "kind": AcceptanceScenarioKind.FINAL_DELIVERY_PRECHECK,
            "area": AcceptanceAreaKind.RELEASE_CANDIDATE,
            "name": "Final Delivery Precheck",
            "evidence": ["final_delivery_precheck_report.json"]
        }
    ]

    out = []
    for s in scenarios:
        out.append(AcceptanceScenario(
            scenario_id=create_acceptance_scenario_id(),
            created_at_utc=generate_timestamp(),
            scenario_kind=s["kind"],
            area_kind=s["area"],
            name=s["name"],
            required=True,
            enabled=True,
            dry_run=True,
            local_fixture_only=True,
            expected_evidence=s["evidence"],
            forbidden_actions=base_forbidden,
            scenario_valid=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return out

def compute_acceptance_scenario_matrix_hash(matrix: AcceptanceScenarioMatrix) -> str:
    data = []
    for s in matrix.scenarios:
        data.append({
            "kind": s.scenario_kind.value,
            "area": s.area_kind.value,
            "name": s.name,
            "enabled": s.enabled
        })
    s = json.dumps(data, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()

def validate_acceptance_scenario_matrix(matrix: AcceptanceScenarioMatrix) -> List[str]:
    errors = []
    if not matrix.matrix_valid:
        errors.append("Matrix is invalid")
    if not matrix.dry_run_only:
        errors.append("Matrix must be dry_run_only")
    if not matrix.local_fixture_only:
        errors.append("Matrix must be local_fixture_only")
    for s in matrix.scenarios:
        if not s.dry_run:
            errors.append(f"Scenario {s.name} is not dry_run")
        if not s.local_fixture_only:
            errors.append(f"Scenario {s.name} is not local_fixture_only")
    return errors

def build_acceptance_scenario_matrix() -> AcceptanceScenarioMatrix:
    scenarios = build_default_acceptance_scenarios()

    matrix = AcceptanceScenarioMatrix(
        matrix_id=create_acceptance_scenario_matrix_id(),
        created_at_utc=generate_timestamp(),
        scenarios=scenarios,
        scenario_count=len(scenarios),
        required_scenario_count=sum(1 for s in scenarios if s.required),
        enabled_scenario_count=sum(1 for s in scenarios if s.enabled),
        matrix_hash=None,
        matrix_valid=True,
        dry_run_only=True,
        local_fixture_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    matrix.matrix_hash = compute_acceptance_scenario_matrix_hash(matrix)
    return matrix

def acceptance_scenario_matrix_to_text(matrix: AcceptanceScenarioMatrix, limit: int = 300) -> str:
    lines = [f"Scenario Matrix: {matrix.matrix_id}"]
    for s in matrix.scenarios[:limit]:
        lines.append(f" - {s.name} ({s.scenario_kind.value})")
    return "\n".join(lines)
