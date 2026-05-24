import os

path1 = "usa_signal_bot/paper_mode_dry_admission_dossier/rehearsal_blocker_rules.py"
content1 = """from typing import Any
import datetime

from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType, PaperModeRehearsalBlockerAction, DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerRule, create_rehearsal_blocker_rule_id

def dangerous_rehearsal_attempt_types() -> list[PaperModeRehearsalAttemptType]:
    return [
        PaperModeRehearsalAttemptType.START_PAPER_MODE_REHEARSAL,
        PaperModeRehearsalAttemptType.START_LOCAL_PAPER_REHEARSAL_RUNTIME,
        PaperModeRehearsalAttemptType.REHEARSE_CANDIDATE,
        PaperModeRehearsalAttemptType.ADMIT_CANDIDATE_TO_REHEARSAL,
        PaperModeRehearsalAttemptType.CREATE_REHEARSAL_SESSION,
        PaperModeRehearsalAttemptType.CREATE_PAPER_SESSION,
        PaperModeRehearsalAttemptType.CREATE_PAPER_ORDER,
        PaperModeRehearsalAttemptType.COMMIT_PAPER_STATE,
        PaperModeRehearsalAttemptType.PATCH_PAPER_CONFIG,
        PaperModeRehearsalAttemptType.SEND_BROKER_ORDER,
        PaperModeRehearsalAttemptType.SEND_TELEGRAM_REAL,
        PaperModeRehearsalAttemptType.UNLOCK_REHEARSAL_GATE
    ]

def rule_for_rehearsal_attempt(attempt_type: PaperModeRehearsalAttemptType) -> PaperModeRehearsalBlockerRule:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    flags = [DryAdmissionDossierRiskFlag.PAPER_MODE_REHEARSAL_RISK]

    if attempt_type == PaperModeRehearsalAttemptType.SEND_BROKER_ORDER:
        flags.append(DryAdmissionDossierRiskFlag.BROKER_ORDER_RISK)
    elif attempt_type == PaperModeRehearsalAttemptType.COMMIT_PAPER_STATE:
        flags.append(DryAdmissionDossierRiskFlag.PAPER_STATE_MUTATION_RISK)
    elif attempt_type == PaperModeRehearsalAttemptType.PATCH_PAPER_CONFIG:
        flags.append(DryAdmissionDossierRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    elif attempt_type == PaperModeRehearsalAttemptType.SEND_TELEGRAM_REAL:
        flags.append(DryAdmissionDossierRiskFlag.TELEGRAM_REAL_SEND_RISK)

    return PaperModeRehearsalBlockerRule(
        rule_id=create_rehearsal_blocker_rule_id(),
        created_at_utc=now,
        attempt_type=attempt_type,
        enabled=True,
        blocking=True,
        action=PaperModeRehearsalBlockerAction.DENY_AND_RECORD,
        description=f"Block {attempt_type.value}",
        risk_flags=flags,
        warnings=[],
        errors=[],
        metadata={}
    )

def default_rehearsal_blocker_rules() -> list[PaperModeRehearsalBlockerRule]:
    return [rule_for_rehearsal_attempt(t) for t in dangerous_rehearsal_attempt_types()]

def validate_rehearsal_blocker_rules_complete(rules: list[PaperModeRehearsalBlockerRule]) -> list[str]:
    errors = []
    covered = {r.attempt_type for r in rules if r.enabled and r.blocking}
    required = set(dangerous_rehearsal_attempt_types())
    missing = required - covered

    if missing:
        errors.append(f"Missing rules for: {[m.value for m in missing]}")

    return errors

def rehearsal_blocker_rules_summary(rules: list[PaperModeRehearsalBlockerRule]) -> dict[str, Any]:
    return {
        "total": len(rules),
        "enabled": sum(1 for r in rules if r.enabled),
        "blocking": sum(1 for r in rules if r.blocking),
        "complete": len(validate_rehearsal_blocker_rules_complete(rules)) == 0
    }

def rehearsal_blocker_rules_to_text(rules: list[PaperModeRehearsalBlockerRule], limit: int = 100) -> str:
    summary = rehearsal_blocker_rules_summary(rules)
    return f"Rehearsal Blocker Rules (Complete: {summary['complete']}): Total={summary['total']}, Blocking={summary['blocking']}"
"""

path2 = "usa_signal_bot/paper_mode_dry_admission_dossier/final_rehearsal_blocker.py"
content2 = """from typing import Any
import datetime

from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType, PaperModeRehearsalBlockerAction, PaperModeRehearsalBlockerStatus, PaperModeRehearsalBlockerDecision
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerEvent, PaperModeRehearsalBlockerRule, create_rehearsal_blocker_event_id
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import default_rehearsal_blocker_rules

class FinalPaperModeRehearsalBlocker:
    def __init__(self, rules: list[PaperModeRehearsalBlockerRule] | None = None):
        self.rules = rules or default_rehearsal_blocker_rules()

    def validate_blocker_enabled(self) -> list[str]:
        errors = []
        if not self.rules:
            errors.append("No rules configured")
        for rule in self.rules:
            if not rule.enabled or not rule.blocking:
                errors.append(f"Rule {rule.rule_id} is not blocking")
        return errors

    def evaluate_attempt(self, attempt_type: PaperModeRehearsalAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperModeRehearsalBlockerEvent:
        return self.deny_rehearsal_attempt(attempt_type, payload, source_component)

    def deny_rehearsal_attempt(self, attempt_type: PaperModeRehearsalAttemptType, payload: dict[str, Any] | None = None, source_component: str | None = None) -> PaperModeRehearsalBlockerEvent:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        rule = next((r for r in self.rules if r.attempt_type == attempt_type), None)

        flags = rule.risk_flags if rule else []
        action = rule.action if rule else PaperModeRehearsalBlockerAction.DENY

        return PaperModeRehearsalBlockerEvent(
            event_id=create_rehearsal_blocker_event_id(),
            created_at_utc=now,
            attempt_type=attempt_type,
            status=PaperModeRehearsalBlockerStatus.REHEARSAL_ATTEMPT_BLOCKED,
            decision=PaperModeRehearsalBlockerDecision.BLOCK_REHEARSAL,
            action=action,
            blocked=True,
            rehearsal_allowed=False,
            paper_mode_rehearsal_allowed=False,
            shadow_launch_allowed=False,
            paper_mode_launch_allowed=False,
            admission_allowed=False,
            active_paper_enabled=False,
            order_created=False,
            paper_state_mutated=False,
            broker_order_sent=False,
            telegram_real_sent=False,
            config_patched=False,
            source_component=source_component,
            payload_summary={"blocked_payload_keys": list(payload.keys())} if payload else {},
            risk_flags=flags,
            warnings=[],
            errors=[],
            metadata={"rule_applied": rule.rule_id if rule else "default_deny"}
        )

    def rehearsal_allowed(self, attempt_type: PaperModeRehearsalAttemptType) -> bool:
        return False

    def blocker_summary(self, events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
        return {
            "events_evaluated": len(events),
            "events_blocked": sum(1 for e in events if e.blocked),
            "all_blocked": all(e.blocked for e in events) if events else True
        }
"""

path3 = "usa_signal_bot/paper_mode_dry_admission_dossier/rehearsal_attempt_simulator.py"
content3 = """from typing import Any
from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerEvent
from usa_signal_bot.paper_mode_dry_admission_dossier.final_rehearsal_blocker import FinalPaperModeRehearsalBlocker
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import dangerous_rehearsal_attempt_types

def _sim_attempt(blocker: FinalPaperModeRehearsalBlocker | None, attempt_type: PaperModeRehearsalAttemptType) -> PaperModeRehearsalBlockerEvent:
    b = blocker or FinalPaperModeRehearsalBlocker()
    return b.evaluate_attempt(attempt_type, {"simulated": True}, "simulator")

def simulate_start_paper_mode_rehearsal_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.START_PAPER_MODE_REHEARSAL)

def simulate_start_local_paper_rehearsal_runtime_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.START_LOCAL_PAPER_REHEARSAL_RUNTIME)

def simulate_rehearse_candidate_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.REHEARSE_CANDIDATE)

def simulate_admit_candidate_to_rehearsal_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.ADMIT_CANDIDATE_TO_REHEARSAL)

def simulate_create_rehearsal_session_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.CREATE_REHEARSAL_SESSION)

def simulate_create_paper_session_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.CREATE_PAPER_SESSION)

def simulate_create_paper_order_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.CREATE_PAPER_ORDER)

def simulate_commit_paper_state_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.COMMIT_PAPER_STATE)

def simulate_patch_paper_config_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.PATCH_PAPER_CONFIG)

def simulate_send_broker_order_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.SEND_BROKER_ORDER)

def simulate_send_telegram_real_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.SEND_TELEGRAM_REAL)

def simulate_unlock_rehearsal_gate_attempt(blocker: FinalPaperModeRehearsalBlocker | None = None) -> PaperModeRehearsalBlockerEvent:
    return _sim_attempt(blocker, PaperModeRehearsalAttemptType.UNLOCK_REHEARSAL_GATE)

def simulate_rehearsal_attempts(blocker: FinalPaperModeRehearsalBlocker | None = None) -> list[PaperModeRehearsalBlockerEvent]:
    b = blocker or FinalPaperModeRehearsalBlocker()
    return [_sim_attempt(b, t) for t in dangerous_rehearsal_attempt_types()]

def rehearsal_attempt_simulator_summary(events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
    return {
        "simulated": len(events),
        "blocked": sum(1 for e in events if e.blocked)
    }

def rehearsal_attempt_simulator_to_text(events: list[PaperModeRehearsalBlockerEvent], limit: int = 100) -> str:
    summary = rehearsal_attempt_simulator_summary(events)
    return f"Rehearsal Attempt Simulator: {summary['blocked']}/{summary['simulated']} blocked"
"""

path4 = "usa_signal_bot/paper_mode_dry_admission_dossier/rehearsal_blocker_analyzer.py"
content4 = """from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import PaperModeRehearsalBlockerEvent
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag

def rehearsal_blocker_all_attempts_blocked(events: list[PaperModeRehearsalBlockerEvent]) -> bool:
    if not events:
        return False
    return all(e.blocked for e in events)

def rehearsal_blocker_has_unblocked_attempts(events: list[PaperModeRehearsalBlockerEvent]) -> bool:
    return any(not e.blocked for e in events)

def rehearsal_blocker_followups(events: list[PaperModeRehearsalBlockerEvent]) -> list[str]:
    if rehearsal_blocker_has_unblocked_attempts(events):
        return ["INVESTIGATE_UNBLOCKED_REHEARSAL_ATTEMPT"]
    return []

def rehearsal_blocker_requires_followup(events: list[PaperModeRehearsalBlockerEvent]) -> bool:
    return len(rehearsal_blocker_followups(events)) > 0

def rehearsal_blocker_risk_summary(events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
    return {
        "all_blocked": rehearsal_blocker_all_attempts_blocked(events),
        "has_unblocked": rehearsal_blocker_has_unblocked_attempts(events),
        "requires_followup": rehearsal_blocker_requires_followup(events)
    }

def analyze_rehearsal_blocker_events(events: list[PaperModeRehearsalBlockerEvent]) -> dict[str, Any]:
    return rehearsal_blocker_risk_summary(events)

def rehearsal_blocker_analyzer_to_text(payload: dict[str, Any]) -> str:
    all_blocked = payload.get("all_blocked", False)
    return f"Rehearsal Blocker Analyzer: All Blocked = {all_blocked}"
"""

with open(path1, "w") as f:
    f.write(content1)
with open(path2, "w") as f:
    f.write(content2)
with open(path3, "w") as f:
    f.write(content3)
with open(path4, "w") as f:
    f.write(content4)

print("Blocker builder created")
