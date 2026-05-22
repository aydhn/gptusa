# Pre-Paper Rehearsal Limitations

The Pre-Paper Rehearsal system operates strictly as a local evaluation utility to assess candidate behavior safely without altering the system.

## Key Limitations
1. **Metadata-Only Firewall:** The mutation firewall produces metadata and block events without directly interacting with the live runtime or intercepting live networking beyond local boundaries.
2. **Not Activation:** The `Activation-Denied Checkpoint` only records the outcome of the rehearsal; it is strictly not an active paper, live, or demo trading approval.
3. **No External Dependencies:** No broker APIs, external real-time data feeds, real Telegram dispatches, or active paper mutations occur.
4. **No Financial Advice:** Rehearsal reviews, scores, and validation outputs are strictly operational and must not be construed as investment advice or performance guarantees.
