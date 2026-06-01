import re
from pathlib import Path

def patch_enums_fix():
    p = Path("usa_signal_bot/core/enums.py")
    content = p.read_text()

    # Clean up duplicate entries due to escape characters if they were added improperly
    content = content.replace('\\"', '"')

    # Quick deduplication script for NotificationType and AlertType if needed
    lines = content.split('\n')
    out = []
    seen = set()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("BASELINE_ML_SCAFFOLDING_BLOCKED =") or stripped.startswith("EVALUATION_HARNESS_BLOCKED =") or stripped.startswith("MODEL_CARD_DRAFT_BLOCKED =") or stripped.startswith("BASELINE_ML_SCAFFOLDING_REPORT =") or stripped.startswith("EVALUATION_HARNESS_WARNING =") or stripped.startswith("MODEL_CARD_DRAFT_WARNING ="):
            if stripped in seen:
                continue
            seen.add(stripped)
        out.append(line)

    p.write_text('\n'.join(out))

if __name__ == "__main__":
    patch_enums_fix()
