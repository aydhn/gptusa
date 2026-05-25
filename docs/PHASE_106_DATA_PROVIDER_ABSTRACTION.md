# Phase 106 Data Provider Abstraction
Phase 106 initiates the data provider abstraction layer. It consumes the read-only Phase 105 kickoff gate output.
This phase strictly prohibits real network fetching. It builds the context for the abstraction.
Use `python -m usa_signal_bot provider-abstraction-info` to view limits.
Use `python -m usa_signal_bot provider-abstraction-context --write` to write the context.
Use `python -m usa_signal_bot provider-abstraction-review --write` to write the review.
