# Stub for acceptance_evaluator.py


# --- Phase 92 ---
# Phase 92
def evaluate_dry_admission_dossier_quality(payload: dict) -> dict:
    score = 1.0
    if payload.get("status") == "VALIDATED_DRY_ADMISSION_SAFE":
        score += 0.2
    if payload.get("rehearsal_allowed") or payload.get("paper_mode_rehearsal_allowed"):
        score = 0.0
    if payload.get("shadow_launch_allowed") or payload.get("paper_mode_launch_allowed"):
        score = 0.0
    if payload.get("admission_allowed") or payload.get("activation_allowed") or payload.get("transition_allowed"):
        score = 0.0
    if payload.get("order_created") or payload.get("mutation_detected"):
        score = 0.0
    return {"dry_admission_dossier_quality_score": score, "note": "Skor yatırım tavsiyesi değildir."}

def evaluate_dry_admission_acceptance_seal_quality(payload: dict) -> dict:
    score = 1.0
    if payload.get("status") == "VALIDATED":
        score += 0.2
    return {"dry_admission_acceptance_seal_score": score, "note": "Skor yatırım tavsiyesi değildir."}

def evaluate_rehearsal_blocker_quality(payload: dict) -> dict:
    score = 1.0
    if payload.get("all_attempts_blocked"):
        score += 0.2
    return {"rehearsal_blocker_score": score, "note": "Skor yatırım tavsiyesi değildir."}

def evaluate_dry_admission_dossier_continuity_quality(payload: dict) -> dict:
    score = 1.0
    return {"dry_admission_dossier_continuity_score": score, "note": "Skor yatırım tavsiyesi değildir."}

def evaluate_dry_admission_dossier_non_execution_compliance_quality(payload: dict) -> dict:
    score = 1.0
    return {"dry_admission_dossier_non_execution_compliance_score": score, "note": "Skor yatırım tavsiyesi değildir."}
