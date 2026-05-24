import os

def append_to_quality():
    path = "usa_signal_bot/quality/acceptance_evaluator.py"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("def evaluate_acceptance():\n    pass\n")

    with open(path, "r") as f:
        content = f.read()

    to_add = """
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
"""
    if "evaluate_dry_admission_dossier_quality" not in content:
        with open(path, "a") as f:
            f.write(to_add)


def append_to_observability():
    path = "usa_signal_bot/observability/metrics_collector.py"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("class MetricsCollector:\n    def __init__(self):\n        self.metrics = {}\n")

    with open(path, "r") as f:
        content = f.read()

    to_add = """
    def record_dry_admission_dossier_metrics(self, payload: dict):
        self.metrics["latest_dry_admission_dossier_count"] = self.metrics.get("latest_dry_admission_dossier_count", 0) + 1
        if payload.get("status") == "BLOCKED":
            self.metrics["latest_dry_admission_dossier_blocked_count"] = self.metrics.get("latest_dry_admission_dossier_blocked_count", 0) + 1

    def record_dry_admission_acceptance_seal_metrics(self, payload: dict):
        self.metrics["latest_dry_admission_acceptance_seal_count"] = self.metrics.get("latest_dry_admission_acceptance_seal_count", 0) + 1
        if payload.get("status") == "FAILED":
            self.metrics["latest_dry_admission_acceptance_seal_failed_count"] = self.metrics.get("latest_dry_admission_acceptance_seal_failed_count", 0) + 1

    def record_rehearsal_blocker_metrics(self, payload: dict):
        self.metrics["latest_rehearsal_blocker_event_count"] = self.metrics.get("latest_rehearsal_blocker_event_count", 0) + 1
        if payload.get("blocked"):
            self.metrics["latest_rehearsal_attempt_blocked_count"] = self.metrics.get("latest_rehearsal_attempt_blocked_count", 0) + 1
        else:
            self.metrics["latest_rehearsal_attempt_not_blocked_count"] = self.metrics.get("latest_rehearsal_attempt_not_blocked_count", 0) + 1

    def record_dry_admission_dossier_safety_metrics(self, payload: dict):
        flags = payload.get("flags", [])
        self.metrics["latest_dry_admission_dossier_safety_flag_count"] = len(flags)
        self.metrics["dry_admission_dossier_warning_count"] = self.metrics.get("dry_admission_dossier_warning_count", 0) + len(payload.get("warnings", []))
        if payload.get("rehearsal_allowed_violation"):
            self.metrics["latest_rehearsal_allowed_violation_count"] = self.metrics.get("latest_rehearsal_allowed_violation_count", 0) + 1
"""
    if "record_dry_admission_dossier_metrics" not in content:
        content = content.replace("self.metrics = {}", "self.metrics = {}" + to_add)
        with open(path, "w") as f:
            f.write(content)


def append_to_notifications():
    path = "usa_signal_bot/notifications/notification_templates.py"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("from typing import Any\nclass NotificationMessage:\n    pass\n")

    with open(path, "r") as f:
        content = f.read()

    to_add = """
def format_dry_admission_dossier_report_message(review: Any) -> Any:
    msg = NotificationMessage()
    msg.text = f"Dry-Admission Dossier Review Required. Review ID: {review.review_id}"
    return msg

def format_dry_admission_acceptance_seal_warning_message(seals: list) -> Any:
    msg = NotificationMessage()
    msg.text = f"Dry-Admission Acceptance Seal Warning: {len(seals)} seals evaluated."
    return msg

def format_rehearsal_blocker_warning_message(events: list) -> Any:
    msg = NotificationMessage()
    msg.text = f"Rehearsal Blocker Warning: {len(events)} attempts evaluated."
    return msg

def notifications_from_dry_admission_dossier_review(review: Any) -> list:
    return [format_dry_admission_dossier_report_message(review)]
"""
    if "format_dry_admission_dossier_report_message" not in content:
        with open(path, "a") as f:
            f.write(to_add)

if __name__ == "__main__":
    append_to_quality()
    append_to_observability()
    append_to_notifications()
    print("Quality, observability, notifications updated")
