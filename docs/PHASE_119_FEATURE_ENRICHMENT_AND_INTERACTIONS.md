# Phase 119: Feature Enrichment & Interactions

Phase 119 introduces event/quality/calendar-aware feature enrichment and interaction builders.
It uses the Phase 118 advanced feature review as read-only ingestion.
It builds local artifact enrichments and does not constitute a signal engine or strategy activation.

Examples:
- `python -m usa_signal_bot feature-enrichment-info`
- `python -m usa_signal_bot build-enriched-feature-table --write`
- `python -m usa_signal_bot feature-enrichment-review --write`
