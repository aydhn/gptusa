# Staged Non-Executing Paper Readiness Rehearsal

The Staged Non-Executing Paper Readiness Rehearsal sub-system evaluates readiness packages by simulating their execution stages without mutating paper state or generating broker orders. It serves purely as a dry-run metadata generation layer.

### Key Concepts
- **Stage Plans**: Extracted from the Readiness Package. Execution must be strictly disabled.
- **Stage Results**: Output of the deterministic rehearsal.
- **Readiness Rehearsal Run**: The full lifecycle result of rehearsing a package.

### CLI Commands
- `python -m usa_signal_bot readiness-rehearsal-info`
- `python -m usa_signal_bot stage-rehearsal-plan --write`
- `python -m usa_signal_bot stage-rehearsal-run --write`
