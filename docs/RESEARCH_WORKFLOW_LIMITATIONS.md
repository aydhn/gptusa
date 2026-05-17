# Research Workflow Limitations

This document outlines the strict boundaries and limitations of the USA Signal Bot Research Workflow (Phase 65):

1. **Local Metadata Only**: All repair queues, hypotheses, and experiment plans serve exclusively as local text/JSON metadata. They do not trigger background daemon processes.
2. **No Auto-Optimization**: The system strictly avoids dynamic, algorithmic parameter searching or live optimization tools (e.g., hyperopt, Optuna, scikit-learn).
3. **No Automatic Configuration Updates**: Generated `ParameterChangeProposal` elements cannot be pushed to production configs autonomously. `allowed_for_auto_apply` is securely pinned to `False`.
4. **Not Investment Advice**: The text outputs of the experiment planner, repair queue, and acceptance gates are heuristic observations. They do not carry financial guarantees or represent formal investment advice.
5. **No Live Approval**: A "PASS" on an acceptance gate represents statistical robustness over historical sets. It does NOT serve as an authorization for broker routing or live trading execution.
6. **No External Communications**: Notifications remain in `dry-run` or local text formats. Real Telegram payload sending is securely isolated and disabled for research tasks.
