# Final Paper Sandbox Runtime Admission Blocker

## Purpose
Simulates and metadata-blocks any attempt to admit candidates into a paper sandbox runtime.

## Restrictions
- Does **not** execute any sandbox runtimes.
- Does **not** allow paper admission.

## Rule Coverage
- START_PAPER_SANDBOX_RUNTIME
- ADMIT_CANDIDATE_TO_SANDBOX_RUNTIME
- START_SANDBOX_PAPER_SESSION
- CREATE_SANDBOX_PAPER_SESSION
- CREATE_SANDBOX_PAPER_ORDER
- COMMIT_SANDBOX_PAPER_STATE
- PATCH_SANDBOX_RUNTIME_CONFIG
- SEND_SANDBOX_BROKER_ORDER
- SEND_SANDBOX_TELEGRAM_REAL
- UNLOCK_SANDBOX_RUNTIME_ADMISSION_GATE

## CLI Examples
`python -m usa_signal_bot sandbox-runtime-admission-blocker-rules --write`
`python -m usa_signal_bot sandbox-runtime-admission-blocker-evaluate --attempt-type start_paper_sandbox_runtime --write`
`python -m usa_signal_bot sandbox-runtime-admission-attempt-simulate --write`
