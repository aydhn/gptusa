1. **Update Enums, Config, Exceptions, and Health:** (Done)
   - Updated `usa_signal_bot/core/enums.py` with Phase 158 enums (e.g., `FullSystemIntegrationStatus`, `FullSystemIntegrationDecision`, etc.).
   - Updated `usa_signal_bot/core/config_schema.py` and `config/default.yaml` with Phase 158 configurations.
   - Updated `usa_signal_bot/core/exceptions.py` with specific Phase 158 exception classes.
   - Updated `usa_signal_bot/core/health.py` with the required Phase 158 health check functions.
   - Note: Phase 158 enforces a strictly local, dry-run, metadata-only structure.

2. **Implement Data Models:**
   - Create `usa_signal_bot/integration/phase158_models.py` defining the core dataclasses (`Phase158HandoffIngestionResult`, `SystemArtifactInventory`, `IntegrationDependencyGraph`, `E2ERehearsalPlan`, `AcceptanceRehearsalResult`, `Phase159ReadinessGate`, `FullSystemIntegrationContext`, etc.) along with ID generators, to_dict, and basic validation functions.

3. **Implement Integration Subsystems (Ingestion to Handoff):**
   - Create `usa_signal_bot/integration/phase157_handoff_ingestion.py` to ingest the previous phase's read-only output.
   - Create `usa_signal_bot/integration/phase157_handoff_artifact_loader.py` to securely load local JSON payloads.
   - Create `usa_signal_bot/integration/integration_input_resolver.py` to process the artifacts and detect forbidden fields (execution semantics like `target_weight`, `buy_signal`).

4. **Implement System Inventory and Dependency Graph:**
   - Create `usa_signal_bot/integration/system_artifact_inventory.py` to catalog artifacts.
   - Create `usa_signal_bot/integration/integration_dependency_graph.py` to define the dependency edges (data -> features -> regimes -> ML -> backtest -> portfolio).

5. **Implement Integration Boundaries and Rehearsals:**
   - Create `usa_signal_bot/integration/integration_boundary_contract.py` ensuring strong local/dry-run boundaries.
   - Create `usa_signal_bot/integration/e2e_rehearsal_plan.py` defining scenarios (e.g., config load, data provider dry run, ML governance dry run).
   - Create `usa_signal_bot/integration/dry_run_rehearsal_executor.py` to mock the execution steps safely.
   - Create `usa_signal_bot/integration/acceptance_rehearsal_result.py` to aggregate the outcome.

6. **Implement Integration Check Reports:**
   - Create the reporting scripts: `schema_compatibility_report.py`, `cli_integration_report.py`, `config_integration_report.py`, `storage_integration_report.py`, `health_integration_report.py`, `quality_observability_integration_report.py`, and `notification_dry_run_integration_report.py` returning `IntegrationCheckReport` objects.

7. **Implement Governance, Final Gates, and Stores:**
   - Create `usa_signal_bot/integration/integration_safety_boundary.py` (IntegrationSafetyBoundaryResult).
   - Create `usa_signal_bot/integration/final_delivery_preparation_checklist.py`.
   - Create `usa_signal_bot/integration/phase159_readiness_gate.py` to evaluate final conditions for Phase 159 progression.
   - Create `usa_signal_bot/integration/full_system_integration_store.py` for storage logic.
   - Create `usa_signal_bot/integration/full_system_integration_report.py` to assemble the `FullSystemIntegrationFullReview`.
   - Create `usa_signal_bot/integration/full_system_integration_validation.py` and `full_system_integration_reporting.py` for cross-validation and display utilities.

8. **Integrate Adapters and Modules:**
   - Update `usa_signal_bot/app/cli.py` to register the new commands.
   - Create `usa_signal_bot/portfolio/risk_reporting/phase157_models.py` (and relevant stubs) if not fully existent.
   - Update `usa_signal_bot/notifications/notification_templates.py` and `adapters.py`.
   - Update `usa_signal_bot/quality/data_quality_evaluator.py`.
   - Update `usa_signal_bot/observability/metrics_collector.py`.

9. **Create Tests and Fixtures:**
   - Generate sample JSON files in `tests/fixtures/full_system_integration/`.
   - Write standard Pytest unit tests for the core phase logic ensuring safety flags (e.g., `paper_state_mutation_enabled=False`).

10. **Update Documentation and Finalize:**
    - Generate/update the markdown docs in `docs/` reflecting Phase 158's purpose and strict non-execution boundaries.
    - Run the pre-commit instructions, fix any issues, verify pytest execution locally, and complete Phase 158.