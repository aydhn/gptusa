from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
import datetime

from usa_signal_bot.core.enums import (
    MarketBehaviorStatus,
    MarketBehaviorDecision,
    MarketBehaviorProfileKind,
    RegimeBehaviorSummaryKind,
    BehaviorReportSectionKind,
    BehaviorReportFormat,
    BehaviorReportQaStatus,
    BehaviorReportLanguageRiskKind,
    MarketBehaviorReadinessStatus,
    MarketBehaviorReadinessRuleKind,
    MarketBehaviorQuality,
    MarketBehaviorRiskFlag,
    MarketBehaviorReportType
)

def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def create_regime_transition_ingestion_id() -> str:
    return f"ingest-{uuid.uuid4()}"

def create_market_behavior_profile_spec_id() -> str:
    return f"spec-{uuid.uuid4()}"

def create_market_behavior_profile_id() -> str:
    return f"prof-{uuid.uuid4()}"

def create_regime_behavior_summary_id() -> str:
    return f"sum-{uuid.uuid4()}"

def create_regime_diagnostics_interpretation_id() -> str:
    return f"intp-{uuid.uuid4()}"

def create_behavior_report_section_id() -> str:
    return f"sec-{uuid.uuid4()}"

def create_behavior_report_document_id() -> str:
    return f"doc-{uuid.uuid4()}"

def create_behavior_report_qa_result_id() -> str:
    return f"qa-{uuid.uuid4()}"

def create_market_behavior_readiness_rule_id() -> str:
    return f"rule-{uuid.uuid4()}"

def create_market_behavior_readiness_gate_id() -> str:
    return f"gate-{uuid.uuid4()}"

def create_market_behavior_context_id() -> str:
    return f"ctx-{uuid.uuid4()}"

def create_market_behavior_full_review_id() -> str:
    return f"rev-{uuid.uuid4()}"

@dataclass
class RegimeTransitionIngestionResult:
    ingestion_id: str = field(default_factory=create_regime_transition_ingestion_id)
    created_at_utc: str = field(default_factory=_now_utc)
    source_path: Optional[str] = None
    source_review_id: Optional[str] = None
    source_context_id: Optional[str] = None
    available: bool = False
    labeling_ingested: bool = False
    sequences_loaded: bool = False
    transition_matrix_built: bool = False
    persistence_analytics_built: bool = False
    duration_analytics_built: bool = False
    churn_diagnostics_built: bool = False
    stability_diagnostics_built: bool = False
    readiness_gate_ready: bool = False
    ready_for_phase130: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    valid_for_phase130: bool = False
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: (v.value if isinstance(v, (MarketBehaviorRiskFlag,)) else v) for k, v in self.__dict__.items()}

@dataclass
class MarketBehaviorProfileSpec:
    spec_id: str = field(default_factory=create_market_behavior_profile_spec_id)
    created_at_utc: str = field(default_factory=_now_utc)
    profile_name: str = ""
    profile_kind: MarketBehaviorProfileKind = MarketBehaviorProfileKind.UNKNOWN
    required_artifacts: list[str] = field(default_factory=list)
    source_fields: list[str] = field(default_factory=list)
    summary_fields: list[str] = field(default_factory=list)
    deterministic: bool = True
    research_metadata_only: bool = True
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: (v.value if isinstance(v, (MarketBehaviorProfileKind, MarketBehaviorRiskFlag)) else v) for k, v in self.__dict__.items()}

@dataclass
class MarketBehaviorProfile:
    profile_id: str = field(default_factory=create_market_behavior_profile_id)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: Optional[str] = None
    profile_name: str = ""
    profile_kind: MarketBehaviorProfileKind = MarketBehaviorProfileKind.UNKNOWN
    summary: str = ""
    metric_snapshot: dict[str, Any] = field(default_factory=dict)
    diagnostic_notes: list[str] = field(default_factory=list)
    dominant_regime_label: Optional[str] = None
    dominant_transition: Optional[str] = None
    persistence_score: Optional[float] = None
    stability_score: Optional[float] = None
    churn_level: Optional[str] = None
    quality: MarketBehaviorQuality = MarketBehaviorQuality.UNKNOWN
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: (v.value if isinstance(v, (MarketBehaviorProfileKind, MarketBehaviorQuality, MarketBehaviorRiskFlag)) else v) for k, v in self.__dict__.items()}

@dataclass
class RegimeBehaviorSummary:
    summary_id: str = field(default_factory=create_regime_behavior_summary_id)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: Optional[str] = None
    summary_kind: RegimeBehaviorSummaryKind = RegimeBehaviorSummaryKind.UNKNOWN
    title: str = ""
    summary_text: str = ""
    bullet_points: list[str] = field(default_factory=list)
    supporting_metrics: dict[str, Any] = field(default_factory=dict)
    limitations: list[str] = field(default_factory=list)
    quality: MarketBehaviorQuality = MarketBehaviorQuality.UNKNOWN
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: (v.value if isinstance(v, (RegimeBehaviorSummaryKind, MarketBehaviorQuality, MarketBehaviorRiskFlag)) else v) for k, v in self.__dict__.items()}

@dataclass
class RegimeDiagnosticsInterpretation:
    interpretation_id: str = field(default_factory=create_regime_diagnostics_interpretation_id)
    created_at_utc: str = field(default_factory=_now_utc)
    symbol: Optional[str] = None
    interpretation_name: str = ""
    source_diagnostic_kind: str = ""
    interpretation_text: str = ""
    confidence_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    data_quality_notes: list[str] = field(default_factory=list)
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: (v.value if isinstance(v, (MarketBehaviorRiskFlag,)) else v) for k, v in self.__dict__.items()}

@dataclass
class BehaviorReportSection:
    section_id: str = field(default_factory=create_behavior_report_section_id)
    created_at_utc: str = field(default_factory=_now_utc)
    section_kind: BehaviorReportSectionKind = BehaviorReportSectionKind.UNKNOWN
    title: str = ""
    body: str = ""
    bullet_points: list[str] = field(default_factory=list)
    tables: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    qa_status: BehaviorReportQaStatus = BehaviorReportQaStatus.NOT_CHECKED
    language_risks: list[BehaviorReportLanguageRiskKind] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {k: (v.value if isinstance(v, (BehaviorReportSectionKind, BehaviorReportQaStatus, BehaviorReportLanguageRiskKind)) else v) for k, v in self.__dict__.items()}

@dataclass
class BehaviorReportDocument:
    document_id: str = field(default_factory=create_behavior_report_document_id)
    created_at_utc: str = field(default_factory=_now_utc)
    title: str = ""
    format: BehaviorReportFormat = BehaviorReportFormat.UNKNOWN
    sections: list[BehaviorReportSection] = field(default_factory=list)
    source_review_id: Optional[str] = None
    rendered_path: Optional[str] = None
    document_hash: Optional[str] = None
    research_metadata_only: bool = True
    investment_advice: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    qa_status: BehaviorReportQaStatus = BehaviorReportQaStatus.NOT_CHECKED
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (BehaviorReportFormat, BehaviorReportQaStatus, MarketBehaviorRiskFlag)):
                res[k] = v.value
            elif k == "sections":
                res[k] = [s.to_dict() for s in v]
            else:
                res[k] = v
        return res

@dataclass
class BehaviorReportQaRuleResult:
    qa_result_id: str = field(default_factory=create_behavior_report_qa_result_id)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_name: str = ""
    status: BehaviorReportQaStatus = BehaviorReportQaStatus.NOT_CHECKED
    passed: bool = False
    language_risk: Optional[BehaviorReportLanguageRiskKind] = None
    matched_terms: list[str] = field(default_factory=list)
    field_name: Optional[str] = None
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (BehaviorReportQaStatus, BehaviorReportLanguageRiskKind)):
                res[k] = v.value
            else:
                res[k] = v
        return res

@dataclass
class MarketBehaviorReadinessRule:
    rule_id: str = field(default_factory=create_market_behavior_readiness_rule_id)
    created_at_utc: str = field(default_factory=_now_utc)
    rule_kind: MarketBehaviorReadinessRuleKind = MarketBehaviorReadinessRuleKind.UNKNOWN
    name: str = ""
    status: MarketBehaviorReadinessStatus = MarketBehaviorReadinessStatus.NOT_CHECKED
    required: bool = True
    passed: bool = False
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (MarketBehaviorReadinessRuleKind, MarketBehaviorReadinessStatus, MarketBehaviorRiskFlag)):
                res[k] = v.value
            else:
                res[k] = v
        return res

@dataclass
class MarketBehaviorReadinessGate:
    gate_id: str = field(default_factory=create_market_behavior_readiness_gate_id)
    created_at_utc: str = field(default_factory=_now_utc)
    status: MarketBehaviorReadinessStatus = MarketBehaviorReadinessStatus.NOT_CHECKED
    rules: list[MarketBehaviorReadinessRule] = field(default_factory=list)
    report_document: Optional[BehaviorReportDocument] = None
    qa_results: list[BehaviorReportQaRuleResult] = field(default_factory=list)
    ready_for_phase131: bool = False
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (MarketBehaviorReadinessStatus, MarketBehaviorRiskFlag)):
                res[k] = v.value
            elif k == "rules":
                res[k] = [r.to_dict() for r in v]
            elif k == "qa_results":
                res[k] = [q.to_dict() for q in v]
            elif k == "report_document" and v:
                res[k] = v.to_dict()
            else:
                res[k] = v
        return res

@dataclass
class MarketBehaviorContext:
    context_id: str = field(default_factory=create_market_behavior_context_id)
    created_at_utc: str = field(default_factory=_now_utc)
    status: MarketBehaviorStatus = MarketBehaviorStatus.UNKNOWN
    decision: MarketBehaviorDecision = MarketBehaviorDecision.UNKNOWN
    source_regime_transition_review_id: Optional[str] = None
    ingestion: Optional[RegimeTransitionIngestionResult] = None
    profile_specs: list[MarketBehaviorProfileSpec] = field(default_factory=list)
    behavior_profiles: list[MarketBehaviorProfile] = field(default_factory=list)
    behavior_summaries: list[RegimeBehaviorSummary] = field(default_factory=list)
    interpretations: list[RegimeDiagnosticsInterpretation] = field(default_factory=list)
    report_document: Optional[BehaviorReportDocument] = None
    qa_results: list[BehaviorReportQaRuleResult] = field(default_factory=list)
    readiness_gate: Optional[MarketBehaviorReadinessGate] = None
    transition_analytics_ingested: bool = False
    diagnostics_loaded: bool = False
    profile_specs_ready: bool = False
    behavior_profiles_ready: bool = False
    regime_summaries_ready: bool = False
    diagnostics_interpreted: bool = False
    report_built: bool = False
    report_qa_passed: bool = False
    readiness_gate_ready: bool = False
    ready_for_phase131: bool = False
    metadata_only: bool = True
    research_data_only: bool = True
    activation_allowed: bool = False
    strategy_activation_allowed: bool = False
    deployment_allowed: bool = False
    active_paper_enabled: bool = False
    broker_execution_enabled: bool = False
    order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    scraping_enabled: bool = False
    html_parse_enabled: bool = False
    paid_api_enabled: bool = False
    dashboard_enabled: bool = False
    network_default_enabled: bool = False
    model_training_used: bool = False
    model_prediction_used: bool = False
    heavy_ml_dependency_used: bool = False
    produces_trade_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    broker_used: bool = False
    order_created: bool = False
    paper_state_mutated: bool = False
    telegram_real_sent: bool = False
    dashboard_started: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[MarketBehaviorRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (MarketBehaviorStatus, MarketBehaviorDecision, MarketBehaviorRiskFlag)):
                res[k] = v.value
            elif k == "ingestion" and v:
                res[k] = v.to_dict()
            elif k == "profile_specs":
                res[k] = [s.to_dict() for s in v]
            elif k == "behavior_profiles":
                res[k] = [s.to_dict() for s in v]
            elif k == "behavior_summaries":
                res[k] = [s.to_dict() for s in v]
            elif k == "interpretations":
                res[k] = [s.to_dict() for s in v]
            elif k == "report_document" and v:
                res[k] = v.to_dict()
            elif k == "qa_results":
                res[k] = [s.to_dict() for s in v]
            elif k == "readiness_gate" and v:
                res[k] = v.to_dict()
            else:
                res[k] = v
        return res

@dataclass
class MarketBehaviorFullReview:
    review_id: str = field(default_factory=create_market_behavior_full_review_id)
    created_at_utc: str = field(default_factory=_now_utc)
    report_type: MarketBehaviorReportType = MarketBehaviorReportType.UNKNOWN
    ingestion: Optional[RegimeTransitionIngestionResult] = None
    context: Optional[MarketBehaviorContext] = None
    behavior_profiles: list[MarketBehaviorProfile] = field(default_factory=list)
    behavior_summaries: list[RegimeBehaviorSummary] = field(default_factory=list)
    interpretations: list[RegimeDiagnosticsInterpretation] = field(default_factory=list)
    report_document: Optional[BehaviorReportDocument] = None
    qa_results: list[BehaviorReportQaRuleResult] = field(default_factory=list)
    readiness_gate: Optional[MarketBehaviorReadinessGate] = None
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        res = {}
        for k, v in self.__dict__.items():
            if isinstance(v, (MarketBehaviorReportType,)):
                res[k] = v.value
            elif k == "ingestion" and v:
                res[k] = v.to_dict()
            elif k == "context" and v:
                res[k] = v.to_dict()
            elif k == "behavior_profiles":
                res[k] = [s.to_dict() for s in v]
            elif k == "behavior_summaries":
                res[k] = [s.to_dict() for s in v]
            elif k == "interpretations":
                res[k] = [s.to_dict() for s in v]
            elif k == "report_document" and v:
                res[k] = v.to_dict()
            elif k == "qa_results":
                res[k] = [s.to_dict() for s in v]
            elif k == "readiness_gate" and v:
                res[k] = v.to_dict()
            else:
                res[k] = v
        return res

def validate_regime_transition_ingestion_result(res: RegimeTransitionIngestionResult) -> list[str]:
    err = []
    if not res.ready_for_phase130: err.append("ready_for_phase130 must be true")
    if not res.research_data_only: err.append("research_data_only must be true")
    if res.activation_allowed: err.append("activation_allowed must be false")
    if res.strategy_activation_allowed: err.append("strategy_activation_allowed must be false")
    if res.deployment_allowed: err.append("deployment_allowed must be false")
    if res.broker_execution_enabled: err.append("broker_execution_enabled must be false")
    if res.order_creation_enabled: err.append("order_creation_enabled must be false")
    if res.paper_state_mutation_enabled: err.append("paper_state_mutation_enabled must be false")
    if res.telegram_real_send_enabled: err.append("telegram_real_send_enabled must be false")
    if res.scraping_enabled: err.append("scraping_enabled must be false")
    if res.html_parse_enabled: err.append("html_parse_enabled must be false")
    if res.paid_api_enabled: err.append("paid_api_enabled must be false")
    if res.dashboard_enabled: err.append("dashboard_enabled must be false")
    if res.network_default_enabled: err.append("network_default_enabled must be false")
    if res.produces_trade_signal: err.append("produces_trade_signal must be false")
    if res.produces_order_decision: err.append("produces_order_decision must be false")
    if res.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    if res.investment_advice: err.append("investment_advice must be false")
    if res.model_training_used: err.append("model_training_used must be false")
    if res.model_prediction_used: err.append("model_prediction_used must be false")
    if res.heavy_ml_dependency_used: err.append("heavy_ml_dependency_used must be false")
    return err

def validate_market_behavior_profile(prof: MarketBehaviorProfile) -> list[str]:
    err = []
    if not prof.research_metadata_only: err.append("research_metadata_only must be true")
    if prof.investment_advice: err.append("investment_advice must be false")
    if prof.produces_trade_signal: err.append("produces_trade_signal must be false")
    if prof.produces_order_decision: err.append("produces_order_decision must be false")
    if prof.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    return err

def validate_regime_behavior_summary(sum: RegimeBehaviorSummary) -> list[str]:
    err = []
    if not sum.research_metadata_only: err.append("research_metadata_only must be true")
    if sum.investment_advice: err.append("investment_advice must be false")
    if sum.produces_trade_signal: err.append("produces_trade_signal must be false")
    if sum.produces_order_decision: err.append("produces_order_decision must be false")
    if sum.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    return err

def validate_regime_diagnostics_interpretation(inter: RegimeDiagnosticsInterpretation) -> list[str]:
    err = []
    if not inter.research_metadata_only: err.append("research_metadata_only must be true")
    if inter.investment_advice: err.append("investment_advice must be false")
    if inter.produces_trade_signal: err.append("produces_trade_signal must be false")
    if inter.produces_order_decision: err.append("produces_order_decision must be false")
    if inter.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    return err

def validate_behavior_report_document(doc: BehaviorReportDocument) -> list[str]:
    err = []
    if not doc.research_metadata_only: err.append("research_metadata_only must be true")
    if doc.investment_advice: err.append("investment_advice must be false")
    if doc.produces_trade_signal: err.append("produces_trade_signal must be false")
    if doc.produces_order_decision: err.append("produces_order_decision must be false")
    if doc.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    return err

def validate_market_behavior_readiness_gate(gate: MarketBehaviorReadinessGate) -> list[str]:
    err = []
    if not gate.research_data_only: err.append("research_data_only must be true")
    if gate.activation_allowed: err.append("activation_allowed must be false")
    if gate.strategy_activation_allowed: err.append("strategy_activation_allowed must be false")
    if gate.deployment_allowed: err.append("deployment_allowed must be false")
    if gate.model_training_used: err.append("model_training_used must be false")
    if gate.model_prediction_used: err.append("model_prediction_used must be false")
    if gate.produces_trade_signal: err.append("produces_trade_signal must be false")
    if gate.produces_order_decision: err.append("produces_order_decision must be false")
    if gate.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    if gate.investment_advice: err.append("investment_advice must be false")
    if gate.ready_for_phase131:
        if gate.status != MarketBehaviorReadinessStatus.PASSED:
            err.append("ready_for_phase131 is true but status is not PASSED")
    return err

def validate_market_behavior_context(ctx: MarketBehaviorContext) -> list[str]:
    err = []
    if not ctx.research_data_only: err.append("research_data_only must be true")
    if ctx.activation_allowed: err.append("activation_allowed must be false")
    if ctx.strategy_activation_allowed: err.append("strategy_activation_allowed must be false")
    if ctx.deployment_allowed: err.append("deployment_allowed must be false")
    if ctx.broker_execution_enabled: err.append("broker_execution_enabled must be false")
    if ctx.order_creation_enabled: err.append("order_creation_enabled must be false")
    if ctx.paper_state_mutation_enabled: err.append("paper_state_mutation_enabled must be false")
    if ctx.telegram_real_send_enabled: err.append("telegram_real_send_enabled must be false")
    if ctx.scraping_enabled: err.append("scraping_enabled must be false")
    if ctx.html_parse_enabled: err.append("html_parse_enabled must be false")
    if ctx.paid_api_enabled: err.append("paid_api_enabled must be false")
    if ctx.dashboard_enabled: err.append("dashboard_enabled must be false")
    if ctx.network_default_enabled: err.append("network_default_enabled must be false")
    if ctx.produces_trade_signal: err.append("produces_trade_signal must be false")
    if ctx.produces_order_decision: err.append("produces_order_decision must be false")
    if ctx.produces_portfolio_weights: err.append("produces_portfolio_weights must be false")
    if ctx.investment_advice: err.append("investment_advice must be false")
    if ctx.model_training_used: err.append("model_training_used must be false")
    if ctx.model_prediction_used: err.append("model_prediction_used must be false")
    if ctx.heavy_ml_dependency_used: err.append("heavy_ml_dependency_used must be false")
    return err

def validate_market_behavior_full_review(rev: MarketBehaviorFullReview) -> list[str]:
    err = []
    if rev.context:
        err.extend(validate_market_behavior_context(rev.context))
    if rev.ingestion:
        err.extend(validate_regime_transition_ingestion_result(rev.ingestion))
    return err
