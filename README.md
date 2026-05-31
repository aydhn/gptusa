# USA Signal Bot

Current Phase: 137 (ML Dataset Assembly, Train-Validation-Test Split Design and Leakage Audit)

This phase establishes the foundational ML datasets for future experimentation.
It operates strictly as a local, non-executing metadata and dataset assembly layer.
It explicitly forbids:
- ML Model Training
- ML Model Predictions
- Any active broker connections
- Real Telegram sends
- Any web scraping or paid APIs

Run tests: `python -m pytest tests/test_phase137*`
