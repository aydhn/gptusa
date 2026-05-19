# Paper-Shadow Limitations & Disclaimers

It is critical to understand the limitations of the paper-shadow rehearsal subsystem:

1.  **Not Real Execution:** The paper-shadow system is NOT a live or demo trading execution system. It does not interact with any broker API.
2.  **Not Real Orders:** A `ShadowOrderIntent` is purely a simulation metadata object and absolutely not an order sent to a broker.
3.  **Not Real Fills:** A `ShadowFill` is a mathematical simulation of a trade and does not represent real liquidity or execution.
4.  **No Mutation:** Running a shadow rehearsal will NOT mutate your existing paper portfolio state or ledgers.
5.  **No Guarantee:** Simulated performance or a "PASS" result in a shadow rehearsal does NOT guarantee future performance and is NOT a recommendation or approval for live trading.
6.  **Not Financial Advice:** The outputs of this system are for research and operational review only and do not constitute investment advice.
