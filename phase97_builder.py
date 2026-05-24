import os
import re

def append_to_enum():
    path = "usa_signal_bot/core/enums.py"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("from enum import Enum\n\n")

    with open(path, "r") as f:
        content = f.read()

    enums_to_add = """
class DryAdmissionDossierStatus(str, Enum):
    DRAFT = "DRAFT"
    CREATED = "CREATED"
    VALIDATED_DRY_ADMISSION_SAFE = "VALIDATED_DRY_ADMISSION_SAFE"
    REQUEST_CHANGES = "REQUEST_CHANGES"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class DryAdmissionDossierDecision(str, Enum):
    CREATE_DRY_ADMISSION_DOSSIER = "CREATE_DRY_ADMISSION_DOSSIER"
    REQUEST_DRY_ADMISSION_GATE_REFRESH = "REQUEST_DRY_ADMISSION_GATE_REFRESH"
    REQUEST_DRY_ADMISSION_ACCEPTANCE_SEAL_REFRESH = "REQUEST_DRY_ADMISSION_ACCEPTANCE_SEAL_REFRESH"
    REQUEST_REHEARSAL_BLOCKER_REFRESH = "REQUEST_REHEARSAL_BLOCKER_REFRESH"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class DryAdmissionDossierEvidenceStatus(str, Enum):
    FRESH = "FRESH"
    PARTIAL = "PARTIAL"
    STALE = "STALE"
    MISSING = "MISSING"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class DryAdmissionAcceptanceSealStatus(str, Enum):
    DRAFT = "DRAFT"
    CREATED = "CREATED"
    SEALED = "SEALED"
    VALIDATED = "VALIDATED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class DryAdmissionAcceptanceSealDecision(str, Enum):
    SEAL_DRY_ADMISSION_ACCEPTANCE = "SEAL_DRY_ADMISSION_ACCEPTANCE"
    REQUEST_DRY_ADMISSION_GATE_REFRESH = "REQUEST_DRY_ADMISSION_GATE_REFRESH"
    REQUEST_SHADOW_REPLAY_REFRESH = "REQUEST_SHADOW_REPLAY_REFRESH"
    REQUEST_BOARD_EVIDENCE_FREEZE_REFRESH = "REQUEST_BOARD_EVIDENCE_FREEZE_REFRESH"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class PaperModeRehearsalBlockerStatus(str, Enum):
    DRAFT = "DRAFT"
    ENABLED_METADATA_ONLY = "ENABLED_METADATA_ONLY"
    REHEARSAL_ATTEMPT_BLOCKED = "REHEARSAL_ATTEMPT_BLOCKED"
    VALIDATED_BLOCKING = "VALIDATED_BLOCKING"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class PaperModeRehearsalBlockerDecision(str, Enum):
    BLOCK_REHEARSAL = "BLOCK_REHEARSAL"
    BLOCK_AND_REQUEST_MANUAL_REVIEW = "BLOCK_AND_REQUEST_MANUAL_REVIEW"
    REQUEST_BLOCKER_RULE_REFRESH = "REQUEST_BLOCKER_RULE_REFRESH"
    REQUEST_DRY_ADMISSION_SEAL_REFRESH = "REQUEST_DRY_ADMISSION_SEAL_REFRESH"
    REQUEST_DRY_ADMISSION_DOSSIER_REFRESH = "REQUEST_DRY_ADMISSION_DOSSIER_REFRESH"
    REJECT = "REJECT"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class PaperModeRehearsalAttemptType(str, Enum):
    START_PAPER_MODE_REHEARSAL = "START_PAPER_MODE_REHEARSAL"
    START_LOCAL_PAPER_REHEARSAL_RUNTIME = "START_LOCAL_PAPER_REHEARSAL_RUNTIME"
    REHEARSE_CANDIDATE = "REHEARSE_CANDIDATE"
    ADMIT_CANDIDATE_TO_REHEARSAL = "ADMIT_CANDIDATE_TO_REHEARSAL"
    CREATE_REHEARSAL_SESSION = "CREATE_REHEARSAL_SESSION"
    CREATE_PAPER_SESSION = "CREATE_PAPER_SESSION"
    CREATE_PAPER_ORDER = "CREATE_PAPER_ORDER"
    COMMIT_PAPER_STATE = "COMMIT_PAPER_STATE"
    PATCH_PAPER_CONFIG = "PATCH_PAPER_CONFIG"
    SEND_BROKER_ORDER = "SEND_BROKER_ORDER"
    SEND_TELEGRAM_REAL = "SEND_TELEGRAM_REAL"
    UNLOCK_REHEARSAL_GATE = "UNLOCK_REHEARSAL_GATE"
    UNKNOWN = "UNKNOWN"

class PaperModeRehearsalBlockerAction(str, Enum):
    DENY = "DENY"
    DENY_AND_RECORD = "DENY_AND_RECORD"
    BLOCK_SESSION = "BLOCK_SESSION"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    UNKNOWN = "UNKNOWN"

class DryAdmissionDossierRiskFlag(str, Enum):
    REAL_ORDER_RISK = "REAL_ORDER_RISK"
    PAPER_ORDER_RISK = "PAPER_ORDER_RISK"
    BROKER_ORDER_RISK = "BROKER_ORDER_RISK"
    PAPER_STATE_MUTATION_RISK = "PAPER_STATE_MUTATION_RISK"
    PAPER_POSITION_MUTATION_RISK = "PAPER_POSITION_MUTATION_RISK"
    PAPER_PORTFOLIO_MUTATION_RISK = "PAPER_PORTFOLIO_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    PRODUCTION_CONFIG_WRITE_RISK = "PRODUCTION_CONFIG_WRITE_RISK"
    ACTIVE_PAPER_ENABLE_RISK = "ACTIVE_PAPER_ENABLE_RISK"
    PAPER_ADMISSION_RISK = "PAPER_ADMISSION_RISK"
    SHADOW_LAUNCH_RISK = "SHADOW_LAUNCH_RISK"
    PAPER_MODE_LAUNCH_RISK = "PAPER_MODE_LAUNCH_RISK"
    PAPER_MODE_REHEARSAL_RISK = "PAPER_MODE_REHEARSAL_RISK"
    ACTIVATION_ALLOWED_RISK = "ACTIVATION_ALLOWED_RISK"
    ADMISSION_ALLOWED_RISK = "ADMISSION_ALLOWED_RISK"
    TRANSITION_ALLOWED_RISK = "TRANSITION_ALLOWED_RISK"
    ORDER_CREATED_RISK = "ORDER_CREATED_RISK"
    MUTATION_DETECTED_RISK = "MUTATION_DETECTED_RISK"
    DRY_ADMISSION_GATE_FAILED = "DRY_ADMISSION_GATE_FAILED"
    SHADOW_REPLAY_FAILED = "SHADOW_REPLAY_FAILED"
    BOARD_EVIDENCE_FREEZE_FAILED = "BOARD_EVIDENCE_FREEZE_FAILED"
    DRY_ADMISSION_ACCEPTANCE_SEAL_FAILED = "DRY_ADMISSION_ACCEPTANCE_SEAL_FAILED"
    REHEARSAL_BLOCKER_FAILED = "REHEARSAL_BLOCKER_FAILED"
    REHEARSAL_ATTEMPT_NOT_BLOCKED = "REHEARSAL_ATTEMPT_NOT_BLOCKED"
    DOSSIER_EVIDENCE_MISSING = "DOSSIER_EVIDENCE_MISSING"
    DOSSIER_EVIDENCE_STALE = "DOSSIER_EVIDENCE_STALE"
    SECRET_RISK = "SECRET_RISK"
    UNKNOWN = "UNKNOWN"

class DryAdmissionDossierReportType(str, Enum):
    DRY_ADMISSION_DOSSIER_REPORT = "DRY_ADMISSION_DOSSIER_REPORT"
    DRY_ADMISSION_ACCEPTANCE_SEAL_REPORT = "DRY_ADMISSION_ACCEPTANCE_SEAL_REPORT"
    REHEARSAL_BLOCKER_REPORT = "REHEARSAL_BLOCKER_REPORT"
    SAFETY_REVIEW = "SAFETY_REVIEW"
    FULL_DRY_ADMISSION_DOSSIER_REVIEW = "FULL_DRY_ADMISSION_DOSSIER_REVIEW"

"""
    if "DryAdmissionDossierStatus" not in content:
        with open(path, "a") as f:
            f.write(enums_to_add)

    # Add to NotificationType and AlertType if they exist
    if "class NotificationType" in content:
        if "DRY_ADMISSION_DOSSIER_REPORT" not in content:
            content = content.replace('class NotificationType(str, Enum):', 'class NotificationType(str, Enum):\n    DRY_ADMISSION_DOSSIER_REPORT = "DRY_ADMISSION_DOSSIER_REPORT"\n    DRY_ADMISSION_ACCEPTANCE_SEAL_WARNING = "DRY_ADMISSION_ACCEPTANCE_SEAL_WARNING"\n    REHEARSAL_BLOCKER_WARNING = "REHEARSAL_BLOCKER_WARNING"')
            with open(path, "w") as f:
                f.write(content)

    if "class AlertType" in content:
        if "DRY_ADMISSION_DOSSIER_BLOCKED" not in content:
            content = content.replace('class AlertType(str, Enum):', 'class AlertType(str, Enum):\n    DRY_ADMISSION_DOSSIER_BLOCKED = "DRY_ADMISSION_DOSSIER_BLOCKED"\n    DRY_ADMISSION_ACCEPTANCE_SEAL_BLOCKED = "DRY_ADMISSION_ACCEPTANCE_SEAL_BLOCKED"\n    REHEARSAL_BLOCKER_BLOCKED = "REHEARSAL_BLOCKER_BLOCKED"')
            with open(path, "w") as f:
                f.write(content)

def append_to_exceptions():
    path = "usa_signal_bot/core/exceptions.py"
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("class BaseAppError(Exception):\n    pass\n\n")

    with open(path, "r") as f:
        content = f.read()

    exceptions_to_add = """
class PaperModeDryAdmissionDossierError(BaseAppError): pass
class DryAdmissionDossierIngestionError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierEligibilityError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierEvidenceError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierBuilderError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionAcceptanceSealError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionAcceptanceSealValidationError(PaperModeDryAdmissionDossierError): pass
class RehearsalBlockerRuleError(PaperModeDryAdmissionDossierError): pass
class FinalRehearsalBlockerError(PaperModeDryAdmissionDossierError): pass
class RehearsalAttemptSimulatorError(PaperModeDryAdmissionDossierError): pass
class RehearsalBlockerAnalyzerError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierContinuityError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierSafetyValidatorError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierAuditError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierStorageError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierValidationError(PaperModeDryAdmissionDossierError): pass
class DryAdmissionDossierReportingError(PaperModeDryAdmissionDossierError): pass
"""
    if "PaperModeDryAdmissionDossierError" not in content:
        with open(path, "a") as f:
            f.write(exceptions_to_add)

if __name__ == "__main__":
    append_to_enum()
    append_to_exceptions()
    print("Enums and exceptions updated.")
