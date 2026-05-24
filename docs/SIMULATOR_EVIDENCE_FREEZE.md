# Simulator Evidence Freeze

## Overview
The Simulator Evidence Freeze mechanism ensures that all metadata related to past local paper simulator sessions, test results, and reviews are compiled, hashed, and frozen. This effectively seals the operational history before reaching the final handoff stage.

## Mechanism
- **Metadata Only:** Like the rest of Phase 100 components, this process handles pure metadata and performs no operations.
- **Frozen & Immutable:** The resulting bundle is flagged as frozen and immutable. This prevents any subsequent alterations from invalidating the proof.
- **Hashing:** A stable hash is generated over the contents of the bundle.
- **Required Evidence:** The builder mandates specific evidence elements to be present. If any are missing, the bundle is marked `PARTIAL` and progress is halted.

## CLI Usage
- Create a Simulator Evidence Freeze:
  `python -m usa_signal_bot simulator-evidence-freeze --write`
- Validate an existing freeze:
  `python -m usa_signal_bot simulator-evidence-freeze-validate --write`
