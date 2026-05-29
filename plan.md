1. **Explore Existing Config/Enums**: We've used `read_file` tools to understand how `usa_signal_bot/core/enums.py`, `usa_signal_bot/core/exceptions.py`, `usa_signal_bot/core/config_schema.py` and `config/default.yaml` are structured. Also confirmed structure of `usa_signal_bot/app/cli.py`, `usa_signal_bot/core/health.py`, `usa_signal_bot/observability/metrics_collector.py`, `usa_signal_bot/quality/data_quality_evaluator.py`, `usa_signal_bot/notifications/notification_templates.py`. `docs/` and `tests/fixtures/` paths exist.
2. **Update Core Files**:
   - Update `usa_signal_bot/core/enums.py` with Phase 130 enumerations (`MarketBehaviorStatus`, `MarketBehaviorDecision`, `MarketBehaviorProfileKind`, etc.).
   - Update `usa_signal_bot/core/exceptions.py` with Phase 130 specific exception classes.
   - Update `config/default.yaml` with the `market_behavior_reporting`, `phase130_behavior_policy`, `phase130_report_policy`, and `phase130_notifications` blocks.
   - Update `usa_signal_bot/core/config_schema.py` with the corresponding dataclasses for the config updates.
3. **Verify Core File Updates**: Check syntax via `python -m py_compile` and verify diffs for safety.
4. **Build Phase 130 Models**: Create `usa_signal_bot/regime_classification/behavior_reporting/phase130_models.py` featuring all the Phase 130 dataclasses and serialization logic.
5. **Implement Logic Modules 1 (Ingestion & Loading)**:
   - Create `usa_signal_bot/regime_classification/behavior_reporting/regime_transition_ingestion.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/diagnostics_artifact_loader.py`
6. **Implement Logic Modules 2 (Profiles & Summaries)**:
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_profile_specs.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_profile_builder.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/regime_behavior_summary_builder.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/diagnostics_interpretation_builder.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/cross_symbol_behavior_profiles.py`
7. **Implement Logic Modules 3 (Reports & Renderers)**:
   - Create `usa_signal_bot/regime_classification/behavior_reporting/behavior_report_sections.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/behavior_report_document.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/markdown_behavior_report_renderer.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/json_behavior_report_renderer.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/text_behavior_report_renderer.py`
8. **Implement Logic Modules 4 (Validation & Gates)**:
   - Create `usa_signal_bot/regime_classification/behavior_reporting/behavior_report_qa_validator.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/behavior_report_readiness_gate.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_safety_validator.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_validation.py`
9. **Implement Logic Modules 5 (Store & Main)**:
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_store.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_reporting.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/market_behavior_report.py`
   - Create `usa_signal_bot/regime_classification/behavior_reporting/__init__.py`
10. **Verify Module Creation**: Run `ls -la usa_signal_bot/regime_classification/behavior_reporting/` to verify all files were created successfully.
11. **Integrate Health & CLI**:
    - Update `usa_signal_bot/core/health.py` with Phase 130 checks.
    - Update `usa_signal_bot/app/cli.py` to register the new commands.
12. **Integrate Observability, Quality, & Notifications**:
    - Update `usa_signal_bot/observability/metrics_collector.py`
    - Update `usa_signal_bot/quality/data_quality_evaluator.py`
    - Update `usa_signal_bot/notifications/notification_templates.py`
13. **Verify Integration File Updates**: Check syntax of `health.py`, `cli.py`, `metrics_collector.py`, `data_quality_evaluator.py`, `notification_templates.py` via `python -m py_compile`.
14. **Documentation 1**:
    - Create `docs/PHASE_130_MARKET_BEHAVIOR_PROFILING.md`
    - Create `docs/MARKET_BEHAVIOR_PROFILES.md`
15. **Documentation 2**:
    - Create `docs/REGIME_BEHAVIOR_SUMMARY.md`
    - Create `docs/REGIME_DIAGNOSTICS_REPORT_LAYER.md`
16. **Documentation 3**:
    - Create `docs/BEHAVIOR_REPORT_QA_AND_LANGUAGE_SAFETY.md`
    - Create `docs/MARKET_BEHAVIOR_SAFETY_GUARDS.md`
17. **Documentation 4**:
    - Create `docs/PHASE_130_LIMITATIONS.md`
    - Create `docs/PHASE_130_SUMMARY.md`
18. **Verify Docs**: `ls -la docs/` to verify file creation.
19. **Create Test Fixtures**:
    - Make directory `tests/fixtures/market_behavior/`
    - Create required fixture files inside (`sample_regime_transition_review.json`, `sample_transition_matrices.json`, `sample_persistence_profiles.json`, `sample_duration_profiles.json`, `sample_churn_diagnostics.json`, `sample_stability_diagnostics.json`, `sample_labeled_regime_table_aapl.csv`, `sample_behavior_report_safe.md`, etc.)
20. **Test Implementation 1**: Create `tests/test_phase130_models.py`, `tests/test_regime_transition_ingestion.py`, `tests/test_diagnostics_artifact_loader.py`
21. **Test Implementation 2**: Create `tests/test_market_behavior_profile_specs.py`, `tests/test_market_behavior_profile_builder.py`, `tests/test_regime_behavior_summary_builder.py`, `tests/test_diagnostics_interpretation_builder.py`
22. **Test Implementation 3**: Create `tests/test_cross_symbol_behavior_profiles.py`, `tests/test_behavior_report_sections.py`, `tests/test_behavior_report_document.py`
23. **Test Implementation 4**: Create `tests/test_markdown_behavior_report_renderer.py`, `tests/test_json_behavior_report_renderer.py`, `tests/test_text_behavior_report_renderer.py`
24. **Test Implementation 5**: Create `tests/test_behavior_report_qa_validator.py`, `tests/test_behavior_report_readiness_gate.py`, `tests/test_market_behavior_safety_validator.py`, `tests/test_market_behavior_report.py`
25. **Test Implementation 6**: Create `tests/test_market_behavior_store.py`, `tests/test_market_behavior_validation.py`, `tests/test_market_behavior_reporting.py`, `tests/test_cli.py` (CLI update test)
26. **Verify Tests**: `ls -la tests/fixtures/market_behavior/` and `ls -la tests/test_*` to verify test creation. Run `pytest` to execute all tests.
27. **Pre-commit**: Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.
28. **Submit**: Use `submit` to push changes.
