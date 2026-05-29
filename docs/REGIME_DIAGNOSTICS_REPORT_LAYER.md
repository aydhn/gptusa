# Regime Diagnostics Report Layer

The report layer is responsible for gathering behavior profiles, summaries, and diagnostics interpretations into a single, cohesive document.

## Structure
- Executive Summary
- Data Scope
- Transition Matrix Summary
- Persistence Summary
- Duration/Churn Summary
- Stability Summary
- Market Behavior Profiles
- Cross-Symbol Behavior
- Diagnostic Interpretation
- Limitations
- Safety Boundary

## Formats
Reports can be rendered in Markdown, JSON, and plain text. These renderers run completely offline without relying on external PDF or third-party formatting dependencies.

## Reproducibility
Every generated report computes a deterministic hash of its content. This ensures integrity tracking and acts as a foundation for Phase 131.
