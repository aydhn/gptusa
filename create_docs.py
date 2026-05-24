import os
from pathlib import Path

docs_to_create = {
    "SHADOW_LAUNCH_BLOCKER_REPLAY.md": """
# Shadow-Launch Blocker Replay
- Shadow-launch blocker replay amacı.
- Replay metadata-only'dir.
- Required shadow-launch attempts.
- blocked=true ve shadow_launch_allowed=false şartı.
- CLI örnekleri:
  - python -m usa_signal_bot shadow-replay-plan --write
  - python -m usa_signal_bot shadow-replay-run --write
  - python -m usa_signal_bot shadow-replay-analyze --write
""",
    "BOARD_EVIDENCE_FREEZE.md": """
# Board Evidence Freeze
- Board evidence freeze amacı.
- Freeze metadata-only'dir.
- Frozen/immutable/hash mantığı.
- Required evidence.
- CLI örnekleri:
  - python -m usa_signal_bot board-evidence-freeze --write
  - python -m usa_signal_bot board-evidence-freeze-validate --write
""",
    "FINAL_PAPER_MODE_DRY_ADMISSION_GATE.md": """
# Final Paper-Mode Dry-Admission Gate
- Final paper-mode dry-admission gate amacı.
- Gate active paper approval değildir.
- Gate paper-mode launch değildir.
- Rule/assertion listesi.
- No-shadow-launch/no-paper-mode-launch/no-order/no-write/no-broker/no-admission/no-activation sınırı.
- CLI örnekleri:
  - python -m usa_signal_bot dry-admission-rules --write
  - python -m usa_signal_bot dry-admission-assertions --write
  - python -m usa_signal_bot final-dry-admission-gate --write
""",
    "DRY_ADMISSION_GATE_SAFETY_GUARDS.md": """
# Dry Admission Gate Safety Guards
- No active paper enable.
- No paper admission.
- No shadow launch.
- No paper-mode launch.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.
- Shadow replay allowed attempt varsa block.
- Board evidence freeze failed/stale ise block.
- Dry-admission assertion failed ise block.
- shadow_launch_allowed true ise block.
- paper_mode_launch_allowed true ise block.
- admission_allowed true ise block.
- activation_allowed true ise block.
- order_created true ise block.
- mutation_detected true ise block.
- CLI örnekleri:
  - python -m usa_signal_bot dry-admission-continuity --write
  - python -m usa_signal_bot dry-admission-safety-check --write
  - python -m usa_signal_bot dry-admission-validate --latest-review
""",
    "DRY_ADMISSION_GATE_LIMITATIONS.md": """
# Dry Admission Gate Limitations
- Dry-admission gate local metadata'dır.
- Shadow replay active paper/live/demo/shadow launch onayı değildir.
- Board evidence freeze deployment değildir.
- Final dry-admission gate gerçek paper runtime değildir.
- Broker API yoktur.
- Paper mutation yoktur.
- Paper order yoktur.
- Telegram real send yoktur.
- Yatırım tavsiyesi değildir.
""",
    "PHASE_96_SUMMARY.md": """
# Phase 96 Summary
- Dry-admission gate models.
- Board dossier ingestion.
- Eligibility checker.
- Shadow-launch blocker replay plan.
- Shadow-launch blocker replay engine.
- Shadow replay analyzer.
- Board evidence freeze.
- Board evidence freeze validator.
- Dry-admission rules.
- Dry-admission assertions.
- Final paper-mode dry-admission gate.
- Dry-admission gate validator.
- Dry-admission continuity.
- Dry-admission safety validator.
- Dry-admission audit.
- Dry-admission report.
- Board dossier / non-execution board / paper-safe dossier / paper runtime adapters.
- Quality/observability entegrasyonları.
- Storage.
- Validation/reporting.
- CLI komutları.
- Health check.
- Testler.
- No broker/live/demo/no scraping/no paid API/no dashboard/no active paper/no shadow launch/no real order/no paper mutation/no Telegram real send entegrasyonu yapılmadığı.
"""
}

for doc, content in docs_to_create.items():
    p = Path(f"docs/{doc}")
    if not p.exists():
        p.write_text(content.strip() + "\n")
