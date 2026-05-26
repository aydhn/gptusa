1. Update core enums, exceptions, config_schema, and default.yaml for Phase 119.
2. Create Phase 119 Models in feature_engine/enriched_features/phase119_models.py.
3. Create context loaders for event, quality, and calendar metadata.
4. Create enrichment specs for event, quality, calendar, and interactions.
5. Create feature builders for event, quality, calendar-aware features, plus freshness, confidence, and anomaly context.
6. Create interaction schema validator and interaction builder.
7. Create enriched feature table builder and its safety validators.
8. Create feature enrichment report, store, and reporting utilities.
9. Update core/health, observability, notifications, and data_quality evaluators.
10. Update app/cli.py to add the new CLI commands.
11. Write documentation and tests for Phase 119.
