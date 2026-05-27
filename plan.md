1.  **Update Enums, Config, and Exceptions**: Already completed the updates to `usa_signal_bot/core/enums.py`, `usa_signal_bot/core/config_schema.py`, and `usa_signal_bot/core/exceptions.py`. Update `config/default.yaml` with the new configuration blocks.

2.  **Create Models (`phase120_models.py`)**: Create the `Phase 120` data classes as requested: `FeatureEnrichmentIngestionResult`, `FeatureGroupDefinition`, `FeatureGroupProfile`, `FactorComponent`, `FactorCandidateDefinition`, `FactorCompositionSpec`, `FeatureCoverageProfile`, `FeatureRedundancyProfile`, `FeatureStabilityProfile`, `FeatureSelectionMetadata`, `FactorReadinessRule`, `FactorReadinessGate`, `FactorCompositionContext`, and `FactorCompositionFullReview`. Include initialization, dictionary conversion, and validation logic.

3.  **Create Logic Modules (`feature_engine/factor_composition/*.py`)**:
    *   `feature_enrichment_ingestion.py`: Ingest Phase 119 data.
    *   `enriched_feature_table_loader.py`: Load output feature CSV files.
    *   `feature_group_registry.py` & `feature_group_profiler.py`: Categorize and profile columns.
    *   `factor_component_registry.py` & `factor_candidate_registry.py`: Create definitions for candidate factors from groups.
    *   `factor_composition_specs.py`: Combine factors and groups into a spec.
    *   `feature_coverage_analyzer.py`, `feature_missingness_analyzer.py`, `feature_stability_analyzer.py`, `feature_redundancy_analyzer.py`: Provide analytical profile information for each column in the feature dataset.
    *   `feature_selection_metadata.py`: Consolidate stats to produce selection metadata for features.
    *   `factor_readiness_rules.py` & `factor_readiness_gate.py`: Generate and evaluate the readiness gate checks.
    *   `factor_composition_safety_validator.py`: Apply execution and payload safety validation over Phase 120 content.
    *   `factor_composition_store.py`: Handle storage paths, serialization, and retrieval.
    *   `factor_composition_validation.py`: Consolidate rule and schema validation.
    *   `factor_composition_reporting.py` & `factor_composition_report.py`: Output summaries and text representation. Create full review pipeline code.

4.  **Integrate with System Modules**:
    *   `usa_signal_bot/core/health.py`: Add Phase 120 health checks.
    *   `usa_signal_bot/quality/quality_models.py`, `data_quality_evaluator.py`, `acceptance_evaluator.py`: Add `phase120` scores to the quality structures.
    *   `usa_signal_bot/observability/metrics_collector.py`: Add metrics tracking counts and violations.
    *   `usa_signal_bot/notifications/notification_templates.py` & `notification_adapters.py`: Add templates for Factor Composition.
    *   `usa_signal_bot/app/cli.py`: Add CLI commands for Phase 120 (e.g. `factor-composition-info`, `feature-group-registry`, `factor-readiness-gate`).

5.  **Create Documentation (`docs/`)**: Add the required Phase 120 markdown files outlining structure, intent, and safety limitations.

6.  **Add Tests (`tests/`)**:
    *   Add test fixtures for feature enrichments and tables.
    *   Create test files corresponding to all modules to ensure they validate correctly and enforce safety constraints.

7.  **Complete Pre-commit Steps**: Ensure `pre_commit_instructions` tool is followed, checking lint, formatting, tests, and AGENTS.md rules.

8.  **Submit the Change**: Finalize changes using a single commit.
