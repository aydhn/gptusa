# Phase 143: Offline Ensemble Prototype Evaluation

## Overview
Phase 143 implements the offline ensemble prototype evaluation, blend diagnostics, and non-activation ensemble registry layer for the USA Signal Bot.

**This phase is NOT active paper trading, deployment, live inference, or a live daemon.** It operates strictly locally, with no web scraping, no HTML parsing, no real Telegram messaging, no real network requests, and no real broker routing.

## Purpose
- Ingest the Phase 142 `EnsembleScaffoldingFullReview` output in read-only mode.
- Perform ensemble governance and non-activation ensemble boundary verification.
- Run offline predictions strictly as local ML research logic using previously built blend coefficient plans.
- Create blend diagnostics, candidate agreement metrics, and ensemble-vs-candidate comparison artifacts.
- Produce offline ensemble evaluation reports.
- Update the Non-Activation Ensemble Registry with local research metrics, clearly marked as ineligible for live/paper deployment.
- Provide a ready baseline for Phase 144 (model drift and post-ensemble governance).

## CLI Examples
```bash
python -m usa_signal_bot ensemble-prototype-info
python -m usa_signal_bot build-ensemble-prototype-specs --write
python -m usa_signal_bot generate-offline-ensemble-predictions --write
python -m usa_signal_bot build-blend-diagnostics --write
python -m usa_signal_bot ensemble-prototype-review --write
```
