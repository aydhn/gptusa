# Regime Map Limitations

**CRITICAL DISCLAIMERS AND LIMITATIONS**

1. **Heuristic Nature:**
   The Regime Map is a heuristic rule-based engine. It is not an ML model, and it is not a crystal ball. Its classifications are approximations of historical states.

2. **Not Investment Advice:**
   The output of the regime map (e.g. `CONFIRMED`, `ALIGNED`, `HIGH RISK`) does **NOT** constitute financial or investment advice.

3. **Not a Live Approval:**
   A `CONFIRMED` status does not mean a trade is guaranteed to be profitable, nor does it act as an automated approval to route an order to a real broker.

4. **No Broker Execution:**
   This subsystem operates entirely in local dry-run / research mode. It has no integration with live brokers, no live order routing, and uses no external telemetry.

5. **No Paid Data APIs:**
   Because this project explicitly prohibits paid APIs, the "Sector Dispersion" feature operates entirely on whatever free metadata is locally available or defaults to symbol-level cross-sectional dispersion.

6. **Transition Risks are not Definitive:**
   Detecting `LOW_VOL_TO_HIGH_VOL` or `BREADTH_RISK_ON_TO_OFF` simply describes the mathematical shift in the recent data window. It does not definitively predict a market crash.
