# PHASE 111 - MACRO, CALENDAR AND NEWS METADATA INTEGRATION SKELETONS

Phase 111 is the metadata skeleton phase.
It introduces read-only ingestion of Phase 110 Provider Orchestration Full Review.
It adopts a metadata-only approach for macro, economic calendar, earnings calendar, corporate actions, and news.

**Important:** Phase 111 is NOT an activation phase.
Events are not trade signals. There is no broker execution, no paper trading, no Telegram real sends, no scraping, no HTML parsing, and no network fetching for news content.

## CLI Commands
- `python -m usa_signal_bot event-metadata-info`
- `python -m usa_signal_bot macro-metadata-catalog`
- `python -m usa_signal_bot event-metadata-review --write`
