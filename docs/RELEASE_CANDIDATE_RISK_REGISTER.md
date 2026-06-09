# Release Candidate Risk Register

Identifies blocking risks:
- Execution violations (broker access, live trading).
- Data access violations (scraping, HTML parsing, real network fetches).
- Mutation violations (paper state mutation, production patches).

If any blocking risk is present, the release candidate is rejected.
