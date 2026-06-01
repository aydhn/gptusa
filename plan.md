1. *Create missing files in `docs` directory.*
   - Create documentation files: `PHASE_139_LOCAL_BASELINE_ML_TRAINING.md`, `BASELINE_TRAINING_JOBS.md`, `OFFLINE_BASELINE_TRAINERS.md`, `OFFLINE_PREDICTION_ARTIFACTS.md`, `OFFLINE_EVALUATION_METRICS.md`, `NON_ACTIVATION_MODEL_REGISTRY.md`, `BASELINE_MODEL_CARD_UPDATES.md`, `BASELINE_TRAINING_SAFETY_GUARDS.md`, `PHASE_139_LIMITATIONS.md`, `PHASE_139_SUMMARY.md`.

2. *Update `core` module.*
   - Append new enums in `usa_signal_bot/core/enums.py`.
   - Update config dataclasses in `usa_signal_bot/core/config_schema.py`.
   - Add new exceptions in `usa_signal_bot/core/exceptions.py`.
   - Add new config keys in `usa_signal_bot/core/config.py` and `config/default.yaml`.
   - Add new health checks in `usa_signal_bot/core/health.py`.
   - Ensure backwards compatibility in all `core` updates.

3. *Update `app`, `quality`, `observability`, and `notifications` modules.*
   - Add CLI commands to `usa_signal_bot/app/cli.py`.
   - Add quality scorecard attributes in `usa_signal_bot/quality/quality_models.py` and update evaluators.
   - Add metric attributes in `usa_signal_bot/observability/metrics_collector.py`.
   - Add notification templates in `usa_signal_bot/notifications/notification_templates.py`.

4. *Create `baseline_training` module files in `usa_signal_bot/ml_research/baseline_training`.*
   - Implement dataclasses in `phase139_models.py`.
   - Implement scaffolding ingestion in `baseline_scaffolding_ingestion.py`.
   - Implement scaffolding artifact loader in `baseline_scaffolding_artifact_loader.py`.
   - Implement dataset loader in `baseline_dataset_loader.py`.
   - Implement training job builder in `baseline_training_job_builder.py`.
   - Implement offline trainers in `baseline_trainers.py` (Dummy, Persistence, Moving Average, Lightweight Linear).
   - Implement offline prediction generator in `offline_prediction_generator.py`.
   - Implement offline evaluation metrics calculator in `offline_evaluation_metrics.py`.
   - Implement offline evaluation report in `offline_evaluation_report.py`.
   - Implement non-activation model registry in `non_activation_model_registry.py`.
   - Implement model card updater in `model_card_updater.py`.
   - Implement baseline training boundary in `baseline_training_boundary.py`.
   - Implement baseline training readiness gate in `baseline_training_readiness_gate.py`.
   - Implement schema validator in `baseline_training_schema_validator.py`.
   - Implement safety validator in `baseline_training_safety_validator.py`.
   - Implement training report in `baseline_training_report.py`.
   - Implement training store in `baseline_training_store.py`.
   - Implement training validation in `baseline_training_validation.py`.
   - Implement training reporting in `baseline_training_reporting.py`.
   - Add `README.md` for the module.

5. *Create Test fixtures and modules.*
   - Create test fixtures in `tests/fixtures/ml_baseline_training`.
   - Create test modules in `tests/` to verify logic and models.

6. *Verify implementation.*
   - Check there are no heavy ML dependencies (sklearn, torch, xgboost, etc).
   - Ensure the phase produces no execution language, no live/broker/paper interaction, only offline baseline ML training and non-activation registry updates.
   - Complete pre-commit step using `pre_commit_instructions` tool.
   - Run `pytest` to confirm successful implementation of Phase 139.

7. *Complete pre commit steps*
   - Complete pre commit steps to make sure proper testing, verifications, reviews and reflections are done.
