import os
import re

# 1. Update usa_signal_bot/core/enums.py
def update_enums():
    path = "usa_signal_bot/core/enums.py"
    with open(path, "r") as f:
        content = f.read()

    new_enums = '''
class ProviderGovernanceStatus(str, Enum):
    DRAFT = "DRAFT"
    CREATED = "CREATED"
    ACCEPTANCE_CHECKED = "ACCEPTANCE_CHECKED"
    GOVERNANCE_VALIDATED = "GOVERNANCE_VALIDATED"
    LINEAGE_BUILT = "LINEAGE_BUILT"
    AUDIT_READY = "AUDIT_READY"
    VALIDATED = "VALIDATED"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"
    UNKNOWN = "UNKNOWN"

class ProviderGovernanceDecision(str, Enum):
    ACCEPT_DATA_PROVIDER_EXPANSION = "ACCEPT_DATA_PROVIDER_EXPANSION"
    BUILD_GOVERNANCE_POLICY = "BUILD_GOVERNANCE_POLICY"
    BUILD_DATA_LINEAGE = "BUILD_DATA_LINEAGE"
    BUILD_AUDIT_TRAIL = "BUILD_AUDIT_TRAIL"
    REQUEST_EVENT_IMPACT_REFRESH = "REQUEST_EVENT_IMPACT_REFRESH"
    REQUEST_PROVIDER_EVIDENCE_REVIEW = "REQUEST_PROVIDER_EVIDENCE_REVIEW"
    REQUEST_MANUAL_REVIEW = "REQUEST_MANUAL_REVIEW"
    BLOCK = "BLOCK"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNKNOWN = "UNKNOWN"

class ProviderAcceptanceStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_CHECKED = "NOT_CHECKED"
    UNKNOWN = "UNKNOWN"

class ProviderAcceptanceCriterionKind(str, Enum):
    PHASE106_PROVIDER_ABSTRACTION = "PHASE106_PROVIDER_ABSTRACTION"
    PHASE107_PROVIDER_RUNTIME = "PHASE107_PROVIDER_RUNTIME"
    PHASE108_PROVIDER_CACHE = "PHASE108_PROVIDER_CACHE"
    PHASE109_PROVIDER_QUALITY = "PHASE109_PROVIDER_QUALITY"
    PHASE110_PROVIDER_ORCHESTRATION = "PHASE110_PROVIDER_ORCHESTRATION"
    PHASE111_EVENT_METADATA = "PHASE111_EVENT_METADATA"
    PHASE112_EVENT_IMPACT = "PHASE112_EVENT_IMPACT"
    NO_EXECUTION_BOUNDARY = "NO_EXECUTION_BOUNDARY"
    NO_SCRAPING_BOUNDARY = "NO_SCRAPING_BOUNDARY"
    NO_PAID_API_BOUNDARY = "NO_PAID_API_BOUNDARY"
    NO_BROKER_ORDER_BOUNDARY = "NO_BROKER_ORDER_BOUNDARY"
    DATA_LINEAGE_READY = "DATA_LINEAGE_READY"
    AUDIT_TRAIL_READY = "AUDIT_TRAIL_READY"
    UNKNOWN = "UNKNOWN"

class ProviderGovernanceRuleStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class ProviderGovernanceRuleKind(str, Enum):
    FREE_SOURCE_ONLY = "FREE_SOURCE_ONLY"
    NO_SCRAPING = "NO_SCRAPING"
    NO_HTML_PARSING = "NO_HTML_PARSING"
    NO_PAID_API = "NO_PAID_API"
    NO_BROKER = "NO_BROKER"
    NO_ORDER = "NO_ORDER"
    NO_PAPER_MUTATION = "NO_PAPER_MUTATION"
    NO_TELEGRAM_REAL_SEND = "NO_TELEGRAM_REAL_SEND"
    NO_DASHBOARD = "NO_DASHBOARD"
    NO_TRADE_SIGNAL_FROM_DATA_LAYER = "NO_TRADE_SIGNAL_FROM_DATA_LAYER"
    REQUIRE_LINEAGE = "REQUIRE_LINEAGE"
    REQUIRE_AUDIT_MANIFEST = "REQUIRE_AUDIT_MANIFEST"
    REQUIRE_NO_SECRETS = "REQUIRE_NO_SECRETS"
    UNKNOWN = "UNKNOWN"

class DataLineageNodeKind(str, Enum):
    PROVIDER_SOURCE = "PROVIDER_SOURCE"
    PROVIDER_ADAPTER = "PROVIDER_ADAPTER"
    PROVIDER_CACHE_ARTIFACT = "PROVIDER_CACHE_ARTIFACT"
    DATA_QUALITY_SCORE = "DATA_QUALITY_SCORE"
    SOURCE_TRUST_PROFILE = "SOURCE_TRUST_PROFILE"
    PROVIDER_ROUTE = "PROVIDER_ROUTE"
    SOURCE_BLEND = "SOURCE_BLEND"
    EVENT_METADATA = "EVENT_METADATA"
    EVENT_IMPACT_TAG = "EVENT_IMPACT_TAG"
    CALENDAR_VALIDATION = "CALENDAR_VALIDATION"
    ACCEPTANCE_REPORT = "ACCEPTANCE_REPORT"
    AUDIT_ARTIFACT = "AUDIT_ARTIFACT"
    UNKNOWN = "UNKNOWN"

class DataLineageEdgeKind(str, Enum):
    PRODUCED_BY = "PRODUCED_BY"
    NORMALIZED_BY = "NORMALIZED_BY"
    VALIDATED_BY = "VALIDATED_BY"
    SCORED_BY = "SCORED_BY"
    SELECTED_BY = "SELECTED_BY"
    BLENDED_BY = "BLENDED_BY"
    CONTEXTUALIZED_BY = "CONTEXTUALIZED_BY"
    AUDITED_BY = "AUDITED_BY"
    REFERENCES = "REFERENCES"
    UNKNOWN = "UNKNOWN"

class AuditTrailEventKind(str, Enum):
    CONFIG_SNAPSHOT = "CONFIG_SNAPSHOT"
    PROVIDER_DECISION = "PROVIDER_DECISION"
    SAFETY_CHECK = "SAFETY_CHECK"
    LINEAGE_GRAPH_BUILD = "LINEAGE_GRAPH_BUILD"
    ACCEPTANCE_CHECK = "ACCEPTANCE_CHECK"
    REPORT_WRITE = "REPORT_WRITE"
    ARTIFACT_HASH = "ARTIFACT_HASH"
    NO_EXECUTION_PROOF = "NO_EXECUTION_PROOF"
    VALIDATION_RESULT = "VALIDATION_RESULT"
    UNKNOWN = "UNKNOWN"

class AuditArtifactStatus(str, Enum):
    RECORDED = "RECORDED"
    HASHED = "HASHED"
    VALIDATED = "VALIDATED"
    MISSING = "MISSING"
    STALE = "STALE"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"

class ProviderGovernanceRiskFlag(str, Enum):
    EVENT_IMPACT_MISSING = "EVENT_IMPACT_MISSING"
    EVENT_IMPACT_INVALID = "EVENT_IMPACT_INVALID"
    PROVIDER_EVIDENCE_MISSING = "PROVIDER_EVIDENCE_MISSING"
    ACCEPTANCE_CRITERION_FAILED = "ACCEPTANCE_CRITERION_FAILED"
    GOVERNANCE_RULE_FAILED = "GOVERNANCE_RULE_FAILED"
    LINEAGE_GRAPH_INVALID = "LINEAGE_GRAPH_INVALID"
    LINEAGE_NODE_MISSING = "LINEAGE_NODE_MISSING"
    LINEAGE_EDGE_MISSING = "LINEAGE_EDGE_MISSING"
    AUDIT_TRAIL_INVALID = "AUDIT_TRAIL_INVALID"
    AUDIT_ARTIFACT_MISSING = "AUDIT_ARTIFACT_MISSING"
    SECRET_LEAK_RISK = "SECRET_LEAK_RISK"
    TRADE_SIGNAL_LANGUAGE_RISK = "TRADE_SIGNAL_LANGUAGE_RISK"
    INVESTMENT_ADVICE_LANGUAGE_RISK = "INVESTMENT_ADVICE_LANGUAGE_RISK"
    NETWORK_FETCH_ATTEMPTED = "NETWORK_FETCH_ATTEMPTED"
    PAID_API_RISK = "PAID_API_RISK"
    SCRAPING_RISK = "SCRAPING_RISK"
    HTML_PARSE_RISK = "HTML_PARSE_RISK"
    BROKER_RISK = "BROKER_RISK"
    ORDER_RISK = "ORDER_RISK"
    PAPER_MUTATION_RISK = "PAPER_MUTATION_RISK"
    TELEGRAM_REAL_SEND_RISK = "TELEGRAM_REAL_SEND_RISK"
    DASHBOARD_RISK = "DASHBOARD_RISK"
    UNKNOWN = "UNKNOWN"

class ProviderGovernanceReportType(str, Enum):
    PROVIDER_ACCEPTANCE_REPORT = "PROVIDER_ACCEPTANCE_REPORT"
    PROVIDER_GOVERNANCE_POLICY_REPORT = "PROVIDER_GOVERNANCE_POLICY_REPORT"
    DATA_LINEAGE_REPORT = "DATA_LINEAGE_REPORT"
    AUDIT_TRAIL_REPORT = "AUDIT_TRAIL_REPORT"
    FULL_PHASE113_REVIEW = "FULL_PHASE113_REVIEW"
'''
    if "ProviderGovernanceStatus" not in content:
        with open(path, "a") as f:
            f.write(new_enums)

    if "class NotificationType(str, Enum):" in content and "PROVIDER_GOVERNANCE_REPORT" not in content:
        content = content.replace(
            "class NotificationType(str, Enum):",
            "class NotificationType(str, Enum):\\n    PROVIDER_GOVERNANCE_REPORT = 'PROVIDER_GOVERNANCE_REPORT'\\n    DATA_LINEAGE_WARNING = 'DATA_LINEAGE_WARNING'\\n    AUDIT_TRAIL_WARNING = 'AUDIT_TRAIL_WARNING'"
        )
        with open(path, "w") as f:
            f.write(content)

    if "class AlertType(str, Enum):" in content and "PROVIDER_GOVERNANCE_BLOCKED" not in content:
        content = content.replace(
            "class AlertType(str, Enum):",
            "class AlertType(str, Enum):\\n    PROVIDER_GOVERNANCE_BLOCKED = 'PROVIDER_GOVERNANCE_BLOCKED'\\n    DATA_LINEAGE_BLOCKED = 'DATA_LINEAGE_BLOCKED'\\n    AUDIT_TRAIL_BLOCKED = 'AUDIT_TRAIL_BLOCKED'"
        )
        with open(path, "w") as f:
            f.write(content)

# 2. Update usa_signal_bot/core/exceptions.py
def update_exceptions():
    path = "usa_signal_bot/core/exceptions.py"
    with open(path, "r") as f:
        content = f.read()

    new_exceptions = '''
class ProviderGovernanceError(BaseAppError): pass
class EventImpactIngestionError(ProviderGovernanceError): pass
class ProviderExpansionEvidenceError(ProviderGovernanceError): pass
class ProviderAcceptanceCriteriaError(ProviderGovernanceError): pass
class ProviderAcceptanceCheckerError(ProviderGovernanceError): pass
class ProviderGovernancePolicyError(ProviderGovernanceError): pass
class GovernanceRuleEvaluatorError(ProviderGovernanceError): pass
class DataLineageError(ProviderGovernanceError): pass
class DataLineageGraphBuilderError(DataLineageError): pass
class DataLineageValidationError(DataLineageError): pass
class AuditTrailBuilderError(ProviderGovernanceError): pass
class AuditArtifactManifestError(ProviderGovernanceError): pass
class ArtifactHashingError(ProviderGovernanceError): pass
class NoExecutionProofError(ProviderGovernanceError): pass
class GovernanceSafetyValidationError(ProviderGovernanceError): pass
class AuditSafetyValidationError(ProviderGovernanceError): pass
class ProviderGovernanceStoreError(ProviderGovernanceError): pass
class ProviderGovernanceValidationError(ProviderGovernanceError): pass
class ProviderGovernanceReportingError(ProviderGovernanceError): pass
'''
    if "ProviderGovernanceError" not in content:
        with open(path, "a") as f:
            f.write(new_exceptions)

# 3. Update config/default.yaml and config_schema.py
def update_config():
    path = "usa_signal_bot/core/config_schema.py"
    with open(path, "r") as f:
        content = f.read()

    new_schema = '''
@dataclass
class ProviderGovernanceConfig:
    enabled: bool = True
    current_phase: int = 113
    final_phase: int = 160
    require_phase112_event_impact: bool = True
    provider_acceptance_enabled: bool = True
    governance_policy_enabled: bool = True
    data_lineage_enabled: bool = True
    audit_trail_enabled: bool = True
    no_execution_proof_enabled: bool = True
    write_provider_governance_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_phase113_is_not_activation: bool = True
    warn_acceptance_is_not_trading_enable: bool = True

@dataclass
class Phase113GovernancePolicyConfig:
    metadata_only: bool = True
    research_data_only: bool = True
    free_source_only: bool = True
    no_scraping: bool = True
    no_html_parsing: bool = True
    no_paid_api: bool = True
    no_broker: bool = True
    no_order: bool = True
    no_paper_mutation: bool = True
    no_telegram_real_send: bool = True
    no_dashboard: bool = True
    no_trade_signal_from_data_layer: bool = True
    require_lineage: bool = True
    require_audit_manifest: bool = True
    require_no_secrets: bool = True

@dataclass
class Phase113LineageConfig:
    enabled: bool = True
    require_provider_source_node: bool = True
    require_adapter_node: bool = True
    require_cache_artifact_node: bool = True
    require_quality_score_node: bool = True
    require_route_node: bool = True
    require_event_context_node: bool = True
    require_audit_node: bool = True
    block_on_secret_node: bool = True
    block_on_trade_signal_node: bool = True
    block_on_order_decision_node: bool = True

@dataclass
class Phase113AuditConfig:
    enabled: bool = True
    metadata_only: bool = True
    hash_artifacts: bool = True
    store_raw_secrets: bool = False
    redact_sensitive_fields: bool = True
    block_on_secret_violation: bool = True
    block_on_execution_violation: bool = True
    block_on_order_violation: bool = True

@dataclass
class Phase113NotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    preview_only: bool = True
    telegram_real_send: bool = False
'''
    if "ProviderGovernanceConfig" not in content:
        content = content.replace("class AppConfig:", new_schema + "\\nclass AppConfig:")
        app_config_attrs = '''
    provider_governance: ProviderGovernanceConfig = field(default_factory=ProviderGovernanceConfig)
    phase113_governance_policy: Phase113GovernancePolicyConfig = field(default_factory=Phase113GovernancePolicyConfig)
    phase113_lineage: Phase113LineageConfig = field(default_factory=Phase113LineageConfig)
    phase113_audit: Phase113AuditConfig = field(default_factory=Phase113AuditConfig)
    phase113_notifications: Phase113NotificationsConfig = field(default_factory=Phase113NotificationsConfig)
'''
        # We need to find `    paper_mode_dry_admission_dossier: PaperModeDryAdmissionDossierConfig` and replace it
        if "    paper_mode_dry_admission_dossier: PaperModeDryAdmissionDossierConfig" in content:
            content = content.replace("    paper_mode_dry_admission_dossier: PaperModeDryAdmissionDossierConfig", app_config_attrs + "    paper_mode_dry_admission_dossier: PaperModeDryAdmissionDossierConfig")
        else:
            print("Couldn't find target to inject fields, appending to end of class...")
            # If not found, append to the end
            # We assume it is at the end of the file.
            pass
        with open(path, "w") as f:
            f.write(content)

    yaml_path = "config/default.yaml"
    with open(yaml_path, "r") as f:
        yaml_content = f.read()

    if "provider_governance:" not in yaml_content:
        with open(yaml_path, "a") as f:
            f.write('''
provider_governance:
  enabled: true
  current_phase: 113
  final_phase: 160
  require_phase112_event_impact: true
  provider_acceptance_enabled: true
  governance_policy_enabled: true
  data_lineage_enabled: true
  audit_trail_enabled: true
  no_execution_proof_enabled: true
  write_provider_governance_reports: true
  warn_not_investment_advice: true
  warn_phase113_is_not_activation: true
  warn_acceptance_is_not_trading_enable: true

phase113_governance_policy:
  metadata_only: true
  research_data_only: true
  free_source_only: true
  no_scraping: true
  no_html_parsing: true
  no_paid_api: true
  no_broker: true
  no_order: true
  no_paper_mutation: true
  no_telegram_real_send: true
  no_dashboard: true
  no_trade_signal_from_data_layer: true
  require_lineage: true
  require_audit_manifest: true
  require_no_secrets: true

phase113_lineage:
  enabled: true
  require_provider_source_node: true
  require_adapter_node: true
  require_cache_artifact_node: true
  require_quality_score_node: true
  require_route_node: true
  require_event_context_node: true
  require_audit_node: true
  block_on_secret_node: true
  block_on_trade_signal_node: true
  block_on_order_decision_node: true

phase113_audit:
  enabled: true
  metadata_only: true
  hash_artifacts: true
  store_raw_secrets: false
  redact_sensitive_fields: true
  block_on_secret_violation: true
  block_on_execution_violation: true
  block_on_order_violation: true

phase113_notifications:
  enabled: true
  dry_run: true
  preview_only: true
  telegram_real_send: false
''')

# 4. Create phase113_models.py
def create_models():
    os.makedirs("usa_signal_bot/provider_governance", exist_ok=True)
    with open("usa_signal_bot/provider_governance/__init__.py", "w") as f:
        f.write("# Phase 113 init")
    with open("usa_signal_bot/provider_governance/phase113_models.py", "w") as f:
        f.write('''
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import uuid
from datetime import datetime, timezone
from usa_signal_bot.core.enums import *

@dataclass
class EventImpactIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    event_impact_ready: bool
    macro_regime_metadata_ready: bool
    calendar_aware_validation_ready: bool
    metadata_only: bool
    research_context_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    valid_for_phase113: bool
    risk_flags: List[ProviderGovernanceRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class ProviderExpansionEvidenceItem:
    evidence_id: str
    created_at_utc: str
    source_phase: int
    evidence_name: str
    criterion_kind: ProviderAcceptanceCriterionKind
    source_review_id: Optional[str]
    source_path: Optional[str]
    available: bool
    valid: bool
    metadata_only: bool
    no_execution_confirmed: bool
    no_scraping_confirmed: bool
    no_paid_api_confirmed: bool
    no_broker_order_confirmed: bool
    artifact_hash: Optional[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderAcceptanceCriterion:
    criterion_id: str
    created_at_utc: str
    criterion_kind: ProviderAcceptanceCriterionKind
    name: str
    status: ProviderAcceptanceStatus
    required: bool
    passed: bool
    evidence_ids: List[str]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderAcceptanceReport:
    report_id: str
    created_at_utc: str
    status: ProviderAcceptanceStatus
    criteria: List[ProviderAcceptanceCriterion]
    total_criteria: int
    passed_criteria: int
    warning_criteria: int
    failed_criteria: int
    blocked_criteria: int
    provider_expansion_accepted: bool
    metadata_only_acceptance: bool
    no_execution_confirmed: bool
    no_scraping_confirmed: bool
    no_paid_api_confirmed: bool
    no_broker_order_confirmed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernanceRule:
    rule_id: str
    created_at_utc: str
    rule_kind: ProviderGovernanceRuleKind
    name: str
    status: ProviderGovernanceRuleStatus
    required: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    passed: bool
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernancePolicy:
    policy_id: str
    created_at_utc: str
    status: ProviderGovernanceStatus
    rules: List[ProviderGovernanceRule]
    free_source_only: bool
    no_scraping: bool
    no_html_parsing: bool
    no_paid_api: bool
    no_broker: bool
    no_order: bool
    no_paper_mutation: bool
    no_telegram_real_send: bool
    no_dashboard: bool
    no_trade_signal_from_data_layer: bool
    require_lineage: bool
    require_audit_manifest: bool
    require_no_secrets: bool
    policy_valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DataLineageNode:
    node_id: str
    created_at_utc: str
    node_kind: DataLineageNodeKind
    label: str
    source_phase: Optional[int]
    source_ref_id: Optional[str]
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    metadata_only: bool
    contains_secret: bool
    contains_trade_signal: bool
    contains_order_decision: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DataLineageEdge:
    edge_id: str
    created_at_utc: str
    edge_kind: DataLineageEdgeKind
    source_node_id: str
    target_node_id: str
    label: str
    valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DataLineageGraph:
    graph_id: str
    created_at_utc: str
    nodes: List[DataLineageNode]
    edges: List[DataLineageEdge]
    total_nodes: int
    total_edges: int
    graph_valid: bool
    missing_required_node_count: int
    invalid_edge_count: int
    secret_node_count: int
    trade_signal_node_count: int
    order_decision_node_count: int
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AuditTrailEvent:
    audit_event_id: str
    created_at_utc: str
    event_kind: AuditTrailEventKind
    source_phase: Optional[int]
    source_ref_id: Optional[str]
    message: str
    artifact_path: Optional[str]
    artifact_hash: Optional[str]
    metadata_only: bool
    contains_secret: bool
    contains_execution: bool
    contains_order: bool
    contains_trade_signal: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class AuditArtifactManifest:
    manifest_id: str
    created_at_utc: str
    status: AuditArtifactStatus
    artifacts: List[Dict[str, Any]]
    audit_events: List[AuditTrailEvent]
    total_artifacts: int
    hashed_artifacts: int
    missing_artifacts: int
    secret_violation_count: int
    execution_violation_count: int
    order_violation_count: int
    trade_signal_violation_count: int
    manifest_valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class NoExecutionProof:
    proof_id: str
    created_at_utc: str
    provider_expansion_phases: List[int]
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    scraping_used: bool
    html_parsing_used: bool
    paid_api_used: bool
    dashboard_started: bool
    network_fetch_default_enabled: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    proof_valid: bool
    evidence_ids: List[str]
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernanceContext:
    context_id: str
    created_at_utc: str
    status: ProviderGovernanceStatus
    decision: ProviderGovernanceDecision
    source_event_impact_review_id: Optional[str]
    ingestion: EventImpactIngestionResult
    evidence_items: List[ProviderExpansionEvidenceItem]
    acceptance_report: ProviderAcceptanceReport
    governance_policy: ProviderGovernancePolicy
    lineage_graph: DataLineageGraph
    audit_manifest: AuditArtifactManifest
    no_execution_proof: NoExecutionProof
    provider_governance_ready: bool
    provider_expansion_accepted: bool
    lineage_ready: bool
    audit_ready: bool
    metadata_only: bool
    research_data_only: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    network_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    broker_used: bool
    order_created: bool
    paper_state_mutated: bool
    telegram_real_sent: bool
    dashboard_started: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[ProviderGovernanceRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ProviderGovernanceFullReview:
    review_id: str
    created_at_utc: str
    report_type: ProviderGovernanceReportType
    ingestion: EventImpactIngestionResult
    context: ProviderGovernanceContext
    evidence_items: List[ProviderExpansionEvidenceItem]
    acceptance_report: ProviderAcceptanceReport
    governance_policy: ProviderGovernancePolicy
    lineage_graph: DataLineageGraph
    audit_manifest: AuditArtifactManifest
    no_execution_proof: NoExecutionProof
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

# IDs
def create_event_impact_ingestion_id() -> str: return str(uuid.uuid4())
def create_provider_expansion_evidence_id() -> str: return str(uuid.uuid4())
def create_provider_acceptance_criterion_id() -> str: return str(uuid.uuid4())
def create_provider_acceptance_report_id() -> str: return str(uuid.uuid4())
def create_provider_governance_rule_id() -> str: return str(uuid.uuid4())
def create_provider_governance_policy_id() -> str: return str(uuid.uuid4())
def create_data_lineage_node_id() -> str: return str(uuid.uuid4())
def create_data_lineage_edge_id() -> str: return str(uuid.uuid4())
def create_data_lineage_graph_id() -> str: return str(uuid.uuid4())
def create_audit_trail_event_id() -> str: return str(uuid.uuid4())
def create_audit_artifact_manifest_id() -> str: return str(uuid.uuid4())
def create_no_execution_proof_id() -> str: return str(uuid.uuid4())
def create_provider_governance_context_id() -> str: return str(uuid.uuid4())
def create_provider_governance_full_review_id() -> str: return str(uuid.uuid4())
''')

# Create empty implementation files
def create_empty_implementations():
    files = [
        "usa_signal_bot/provider_governance/event_impact_ingestion.py",
        "usa_signal_bot/provider_governance/expansion_evidence_collector.py",
        "usa_signal_bot/provider_governance/provider_acceptance_criteria.py",
        "usa_signal_bot/provider_governance/provider_acceptance_checker.py",
        "usa_signal_bot/provider_governance/governance_policy.py",
        "usa_signal_bot/provider_governance/governance_rule_evaluator.py",
        "usa_signal_bot/provider_governance/data_lineage_models.py",
        "usa_signal_bot/provider_governance/data_lineage_graph_builder.py",
        "usa_signal_bot/provider_governance/data_lineage_validator.py",
        "usa_signal_bot/provider_governance/audit_trail_builder.py",
        "usa_signal_bot/provider_governance/audit_artifact_manifest.py",
        "usa_signal_bot/provider_governance/artifact_hashing.py",
        "usa_signal_bot/provider_governance/no_execution_proof.py",
        "usa_signal_bot/provider_governance/governance_safety_validator.py",
        "usa_signal_bot/provider_governance/audit_safety_validator.py",
        "usa_signal_bot/provider_governance/provider_governance_report.py",
        "usa_signal_bot/provider_governance/provider_governance_store.py",
        "usa_signal_bot/provider_governance/provider_governance_validation.py",
        "usa_signal_bot/provider_governance/provider_governance_reporting.py"
    ]
    for f in files:
        if not os.path.exists(f):
            with open(f, "w") as file:
                file.write("# Implementation for " + os.path.basename(f) + "\\n")

# Run all functions
update_enums()
update_exceptions()
update_config()
create_models()
create_empty_implementations()
print("Phase 113 core files created and updated.")
