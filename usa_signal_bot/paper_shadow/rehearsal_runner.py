from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowRehearsalSession, ShadowPortfolioState,
    ShadowSignal, ShadowOrderIntent, ShadowFill, ShadowPnLSnapshot,
    create_shadow_rehearsal_session_id, get_utc_now_str
)
from usa_signal_bot.core.enums import ShadowSessionStatus, ShadowRuntimeMode, ShadowLedgerEventType
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio, update_shadow_portfolio_with_fill
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_shadow_signals
from usa_signal_bot.paper_shadow.shadow_candidate_selection import select_shadow_candidates
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents, block_real_order_like_intents
from usa_signal_bot.paper_shadow.shadow_risk_gate import apply_shadow_risk_gates
from usa_signal_bot.paper_shadow.shadow_fill_simulator import simulate_shadow_fills
from usa_signal_bot.paper_shadow.shadow_pnl_tracker import update_shadow_pnl_after_fills
from usa_signal_bot.paper_shadow.shadow_rebalance import build_shadow_rebalance_preview
from usa_signal_bot.paper_shadow.shadow_notifications import build_shadow_notification_preview
from usa_signal_bot.paper_shadow.shadow_ledger import create_shadow_ledger_event, append_shadow_ledger_event
from usa_signal_bot.paper_shadow.shadow_safety_guard import assert_shadow_session_safe

class PaperShadowRehearsalRunner:
    def __init__(self, runtime_mode: ShadowRuntimeMode = ShadowRuntimeMode.FULL_PAPER_SHADOW):
        self.runtime_mode = runtime_mode

    def run_rehearsal(self, context: ShadowSimulationContext) -> ShadowRehearsalSession:
        assert_shadow_session_safe(context)

        session = ShadowRehearsalSession(
            session_id=create_shadow_rehearsal_session_id(),
            created_at_utc=get_utc_now_str(),
            status=ShadowSessionStatus.RUNNING,
            context=context,
            portfolio_state=None,
            signals=[],
            order_intents=[],
            fills=[],
            ledger_events=[],
            pnl_snapshots=[],
            safety_flags=[],
            started_at_utc=get_utc_now_str(),
            completed_at_utc=None,
            output_paths={},
            warnings=[],
            errors=[]
        )

        try:
            append_shadow_ledger_event(session.ledger_events, create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {}))

            portfolio = initialize_shadow_portfolio(context)
            session.portfolio_state = portfolio

            signals = self.run_signal_stage(context)
            session.signals = signals

            candidates = self.run_candidate_stage(signals)

            intents = self.run_intent_stage(candidates)
            session.order_intents = intents

            intents = self.run_risk_stage(intents, portfolio, context)

            fills = self.run_fill_stage(intents)
            session.fills = fills

            portfolio = self.run_portfolio_stage(portfolio, fills)
            session.portfolio_state = portfolio

            pnl = self.run_pnl_stage(portfolio, fills, context.starting_equity_usd)
            session.pnl_snapshots.append(pnl)

            self.run_rebalance_stage(portfolio, context)
            self.run_notification_stage(session)

            assert_shadow_session_safe(context, intents, fills)

            append_shadow_ledger_event(session.ledger_events, create_shadow_ledger_event(ShadowLedgerEventType.SESSION_COMPLETED, {}))
            session.status = ShadowSessionStatus.COMPLETED

        except Exception as e:
            session.status = ShadowSessionStatus.FAILED
            session.errors.append(str(e))

        session.completed_at_utc = get_utc_now_str()
        return session

    def run_signal_stage(self, context: ShadowSimulationContext) -> List[ShadowSignal]:
        return generate_shadow_signals(context)

    def run_candidate_stage(self, signals: List[ShadowSignal]) -> List[ShadowSignal]:
        return select_shadow_candidates(signals)

    def run_intent_stage(self, candidates: List[ShadowSignal]) -> List[ShadowOrderIntent]:
        intents = build_shadow_order_intents(candidates)
        return block_real_order_like_intents(intents)

    def run_risk_stage(self, intents: List[ShadowOrderIntent], portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> List[ShadowOrderIntent]:
        return apply_shadow_risk_gates(intents, portfolio, context)

    def run_fill_stage(self, intents: List[ShadowOrderIntent]) -> List[ShadowFill]:
        return simulate_shadow_fills(intents)

    def run_portfolio_stage(self, portfolio: ShadowPortfolioState, fills: List[ShadowFill]) -> ShadowPortfolioState:
        for fill in fills:
            portfolio = update_shadow_portfolio_with_fill(portfolio, fill)
        return portfolio

    def run_pnl_stage(self, portfolio: ShadowPortfolioState, fills: List[ShadowFill], starting_equity_usd: float) -> ShadowPnLSnapshot:
        return update_shadow_pnl_after_fills(portfolio, fills, starting_equity_usd)

    def run_rebalance_stage(self, portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> Dict[str, Any]:
        return build_shadow_rebalance_preview(portfolio, context)

    def run_notification_stage(self, session: ShadowRehearsalSession) -> Dict[str, Any]:
        return build_shadow_notification_preview(session)
