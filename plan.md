1. **Core Enums & Config**: Update `core/enums.py`, `core/config_schema.py`, `config/default.yaml`, `config/local.example.yaml`, `core/exceptions.py`.
2. **Phase 128 Models**: Create `regime_classification/labeling/phase128_models.py`.
3. **Core Modules (Ingestion, Loader, Specs)**: Implement ingestion and input loaders.
4. **Labeling Logic**: Implement specs, rules, resolver, heuristic labeling, conflict/confidence engines.
5. **Rolling Windows & Sequences**: Implement rolling windows, sequences, stability profiles.
6. **Validation & Safety Gates**: Candidate validation, readiness gate, schema/safety validators.
7. **Storage, Reporting, and Full Review**: Implement data access, validation, formatting, and the final context builder.
8. **Integrations**: Add CLI commands, health checks, notifications, quality/observability updates.
9. **Tests & Docs**: Add test fixtures, tests, and documentation files.
