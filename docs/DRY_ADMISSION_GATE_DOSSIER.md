# Dry Admission Gate Dossier

## Purpose
The Dry Admission Gate Dossier serves as a strictly read-only, metadata container that aggregates evidence and checks prior to generating an acceptance seal. It operates exclusively within the local layer.

## Crucial Note
**A Dry Admission Gate Dossier IS NOT an active paper admission, shadow launch, paper-mode launch, or rehearsal.**
It explicitly asserts `activation_allowed=false`, `rehearsal_allowed=false`, `order_created=false` and blocks all state mutations.

## Evidence Items
The dossier collects the following pieces of evidence:
1. `dry_admission_gate_full_review`
2. `final_paper_mode_dry_admission_gate`
3. `shadow_launch_replay_result`
4. `board_evidence_freeze`
5. `dry_admission_rules`
6. `dry_admission_assertions`
7. `dry_admission_continuity`
8. `dry_admission_safety_report`
9. `board_dossier_full_review`
10. `acceptance_board_seal`
11. `shadow_launch_blocker_events`
12. `validation_reports`
13. `audit_trails`

These evidences must be `FRESH` and not `STALE`. They derive from prior safety phases (e.g. final_paper_mode_dry_admission_gate, shadow_launch_replay_result, board_evidence_freeze).

## CLI Examples
```bash
python -m usa_signal_bot dry-admission-dossier-evidence --write
python -m usa_signal_bot dry-admission-dossier --write
python -m usa_signal_bot dry-admission-dossier-review --write
```
