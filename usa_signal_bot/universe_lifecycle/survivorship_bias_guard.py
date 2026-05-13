from typing import List, Optional
import datetime
from usa_signal_bot.core.enums import SymbolLifecycleStatus, SurvivorshipBiasRisk, UniverseGuardStatus
from usa_signal_bot.universe_lifecycle.lifecycle_models import (
    UniverseSnapshot, SurvivorshipBiasAssessment, create_survivorship_assessment_id
)
from usa_signal_bot.universe_lifecycle.symbol_status_resolver import SymbolStatusResolver

class SurvivorshipBiasGuard:
    def __init__(self, resolver: SymbolStatusResolver, historical_snapshots: Optional[List[UniverseSnapshot]] = None):
        self.resolver = resolver
        self.historical_snapshots = historical_snapshots or []

    def _assess_base(self, symbols: List[str], universe_name: str, as_of_date: Optional[str] = None) -> SurvivorshipBiasAssessment:
        records = self.resolver.resolve_many(symbols, as_of_date)
        delisted = sum(1 for r in records if r.status == SymbolLifecycleStatus.DELISTED)
        inactive = sum(1 for r in records if r.status == SymbolLifecycleStatus.INACTIVE)
        unknown = sum(1 for r in records if r.status in [SymbolLifecycleStatus.UNKNOWN, SymbolLifecycleStatus.REVIEW_REQUIRED])
        affected = [r.symbol for r in records if r.status != SymbolLifecycleStatus.ACTIVE]
        assessment = SurvivorshipBiasAssessment(
            assessment_id=create_survivorship_assessment_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            universe_name=universe_name,
            as_of_date=as_of_date,
            status=UniverseGuardStatus.UNKNOWN,
            risk=SurvivorshipBiasRisk.UNKNOWN,
            current_symbol_count=len(symbols),
            delisted_symbol_count=delisted,
            inactive_symbol_count=inactive,
            unknown_status_count=unknown,
            affected_symbols=affected,
            warnings=[]
        )
        return assessment

    def assess_universe(self, symbols: List[str], universe_name: str, as_of_date: Optional[str] = None, current_snapshot: Optional[UniverseSnapshot] = None) -> SurvivorshipBiasAssessment:
        assessment = self._assess_base(symbols, universe_name, as_of_date)
        assessment.risk = self.decide_risk(assessment)
        assessment.status = self.decide_guard_status(assessment)
        if assessment.risk in [SurvivorshipBiasRisk.HIGH, SurvivorshipBiasRisk.CRITICAL]:
            assessment.warnings.append("High survivorship bias risk detected in universe.")
        return assessment

    def assess_backtest_universe(self, symbols: List[str], universe_name: str, backtest_start_date: Optional[str], backtest_end_date: Optional[str]) -> SurvivorshipBiasAssessment:
        assessment = self._assess_base(symbols, universe_name, backtest_start_date)
        if not self.historical_snapshots and backtest_start_date:
            try:
                start_dt = datetime.datetime.fromisoformat(backtest_start_date.replace("Z", "+00:00"))
                if start_dt.tzinfo is None:
                    start_dt = start_dt.replace(tzinfo=datetime.timezone.utc)
                now = datetime.datetime.now(datetime.timezone.utc)
                if (now - start_dt).days > 30:
                    assessment.warnings.append("Historical backtest using current universe without historical snapshots.")
                    if assessment.risk == SurvivorshipBiasRisk.LOW or assessment.risk == SurvivorshipBiasRisk.NONE:
                        assessment.risk = SurvivorshipBiasRisk.HIGH
            except ValueError:
                pass

        risk2 = self.decide_risk(assessment)
        idx1 = list(SurvivorshipBiasRisk).index(assessment.risk) if assessment.risk != SurvivorshipBiasRisk.UNKNOWN else -1
        idx2 = list(SurvivorshipBiasRisk).index(risk2) if risk2 != SurvivorshipBiasRisk.UNKNOWN else -1
        assessment.risk = assessment.risk if idx1 > idx2 else risk2

        assessment.status = self.decide_guard_status(assessment)
        return assessment

    def assess_scan_universe(self, symbols: List[str], universe_name: str) -> SurvivorshipBiasAssessment:
        assessment = self._assess_base(symbols, universe_name, None)
        assessment.risk = self.decide_risk(assessment)
        assessment.status = self.decide_guard_status(assessment)
        return assessment

    def decide_guard_status(self, assessment: SurvivorshipBiasAssessment) -> UniverseGuardStatus:
        if assessment.risk == SurvivorshipBiasRisk.CRITICAL:
            return UniverseGuardStatus.BLOCK_BACKTEST
        elif assessment.risk == SurvivorshipBiasRisk.HIGH:
            return UniverseGuardStatus.WARNING
        elif assessment.unknown_status_count > 0:
            return UniverseGuardStatus.REVIEW_REQUIRED
        elif assessment.delisted_symbol_count > 0:
            return UniverseGuardStatus.BLOCK_SIGNAL
        return UniverseGuardStatus.CLEAR

    def decide_risk(self, assessment: SurvivorshipBiasAssessment) -> SurvivorshipBiasRisk:
        if assessment.current_symbol_count == 0:
            return SurvivorshipBiasRisk.NONE
        pct_unknown = assessment.unknown_status_count / assessment.current_symbol_count
        if assessment.delisted_symbol_count > 0 and not assessment.as_of_date:
            return SurvivorshipBiasRisk.CRITICAL
        if pct_unknown > 0.5:
            return SurvivorshipBiasRisk.HIGH
        elif pct_unknown > 0.1:
            return SurvivorshipBiasRisk.MODERATE
        if assessment.as_of_date and assessment.delisted_symbol_count == 0 and assessment.inactive_symbol_count == 0 and not self.historical_snapshots:
            return SurvivorshipBiasRisk.HIGH
        return SurvivorshipBiasRisk.LOW

    def recommended_guards(self, assessment: SurvivorshipBiasAssessment) -> List[str]:
        guards = []
        if assessment.risk in [SurvivorshipBiasRisk.HIGH, SurvivorshipBiasRisk.CRITICAL]:
            guards.append("use_historical_universe_snapshot")
            guards.append("mark_backtest_survivorship_bias_warning")
            guards.append("do_not_treat_backtest_as_production_evidence")
        if assessment.unknown_status_count > 0:
            guards.append("require_manual_lifecycle_review")
            guards.append("lower_research_quality_score")
            guards.append("exclude_unknown_status_from_strict_backtest")
        if assessment.delisted_symbol_count > 0:
            guards.append("include_delisted_symbols_if_available")
        return guards
