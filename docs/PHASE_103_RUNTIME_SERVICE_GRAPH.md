# Phase 103: Runtime Service Graph

This phase introduces the core infrastructure for generating a local, non-executing service dependency graph.

## Overview
Phase 103 orchestrates the different components built in previous phases into a cohesive metadata structure:
- **Service Nodes:** Abstract representations of system capabilities.
- **Dependency Contracts:** Explicit rules governing what services can talk to each other and what they can do.
- **Service Graph:** A validated directed acyclic graph built from nodes and contracts.

## Key Principles
- **No Active Paper Enablement:** This phase strictly organizes services; it does not launch them into an active paper mode.
- **No Broker Execution:** No orders are sent. No real portfolio data is fetched.
- **Dry-Run Default:** All orchestration and planning built upon the service graph is performed strictly as a metadata dry-run.

## CLI Usage
- `python -m usa_signal_bot service-catalog`
- `python -m usa_signal_bot runtime-service-graph --write`
- `python -m usa_signal_bot service-graph-review --write`
