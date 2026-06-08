# Phase 155 - Inputs and Boundaries

## Overview
Phase 155 consumes inputs from the previous phase (154) and strictly adheres to predefined boundaries to prevent active executions.

## Expected Inputs
- **Sizing Prototype Review:** A serialized validation report containing Phase 154 prototypes.
- **Sizing Policy:** Rules and limits constructed around candidate positioning.
- **Method Contracts:** Agreements on the approach chosen for each dimension.
- **Sizing Comparison Matrix:** Relational metrics across models.
- **Risk Budget Adherence Report:** Diagnostic metrics showing alignment to maximum risk targets.
- **Sizing Safety Boundary:** Non-execution verification rule states.
- **Sandbox Candidate Inputs:** A list or dataframe representing active eligible assets.

## Core Boundaries
- Input processing is purely **read-only**; artifacts are not modified.
- No actual target weight or actual allocation references are processed or generated.
