# Ensemble Prototype Safety Guards

Safety rules enforced at the boundary:
- Offline Prototype Only
- Offline Evaluation Only
- No Trade Signal Output
- No Order Decision Output
- No Portfolio Weight Output
- No Strategy Activation
- No Broker Execution
- No Paper Mutation
- No Telegram Real Send
- No Deployment
- No Dashboard
- No Paid API usage
- No Network Default Allowed
- No Live Inference
- No Online Inference
- No Threshold Optimization
- No Heavy ML Dependencies (sklearn/torch/xgboost prohibited as core dependencies)
- No Daemon/Scheduler usage
- No Secrets leaked
- No Guaranteed Profit Language

Any violations block readiness to transition to Phase 144.
