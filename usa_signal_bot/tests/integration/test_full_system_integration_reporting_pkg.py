import pytest
from usa_signal_bot.integration.phase158_models import (
    Phase158HandoffIngestionResult,
    IntegrationInputReference,
    SystemArtifactInventory,
    IntegrationDependencyGraph,
    IntegrationBoundaryContract,
    E2ERehearsalPlan,
)
from usa_signal_bot.integration.full_system_integration_reporting import (
    phase158_handoff_ingestion_result_to_text,
    integration_input_reference_to_text,
    system_artifact_inventory_to_text,
    integration_dependency_graph_to_text,
    integration_boundary_contract_to_text,
    e2e_rehearsal_plan_to_text,
)

def test_phase158_handoff_ingestion_result_to_text():
    item = Phase158HandoffIngestionResult(valid_for_phase158=True)
    assert phase158_handoff_ingestion_result_to_text(item) == 'Phase158HandoffIngestionResult(valid=True)'

    item2 = Phase158HandoffIngestionResult(valid_for_phase158=False)
    assert phase158_handoff_ingestion_result_to_text(item2) == 'Phase158HandoffIngestionResult(valid=False)'

def test_integration_input_reference_to_text():
    item = IntegrationInputReference(valid=True)
    assert integration_input_reference_to_text(item) == 'IntegrationInputReference(valid=True)'

def test_system_artifact_inventory_to_text():
    item = SystemArtifactInventory(inventory_valid=True)
    assert system_artifact_inventory_to_text(item) == 'SystemArtifactInventory(valid=True)'
    assert system_artifact_inventory_to_text(item, limit=20) == 'SystemArtifactInventory(valid=True)'[:20]

def test_integration_dependency_graph_to_text():
    item = IntegrationDependencyGraph(graph_valid=True)
    assert integration_dependency_graph_to_text(item) == 'IntegrationDependencyGraph(valid=True)'
    assert integration_dependency_graph_to_text(item, limit=10) == 'Integratio'

def test_integration_boundary_contract_to_text():
    item = IntegrationBoundaryContract(contract_valid=True)
    assert integration_boundary_contract_to_text(item) == 'IntegrationBoundaryContract(valid=True)'

def test_e2e_rehearsal_plan_to_text():
    item = E2ERehearsalPlan(plan_valid=True)
    assert e2e_rehearsal_plan_to_text(item) == 'E2ERehearsalPlan(valid=True)'
