# Observer Limitations

To maintain compliance with the project's strict local research governance, the Paper Observer subsystem enforces the following limitations:

1.  **Non-Executing Runtime:** The observer runtime does not execute live trades, paper trades, or demo trades.
2.  **Proposals Are Not Orders:** An `ObserverOutput` of type `PROPOSAL_MIRROR` is local metadata representing an *intent*, and will never be serialized into a broker dispatch format.
3.  **Human Approval Is Not Deployment:** Approval to enter the Paper Observer stage is strictly approval to generate local metadata; it does not grant production permissions.
4.  **No Broker API Integrations:** The subsystem does not call Alpaca, IBKR, Robinhood, or any live broker.
5.  **No Paper Mutation:** The active paper portfolio and execution logs (`paper_store`) are never written to by the observer.
6.  **No Real Telegram Sends:** The observer handles notification payloads solely to generate local string previews.
7.  **Not Investment Advice:** All observer outputs, signals, and drift analyses are localized heuristics and do not constitute financial advice.
