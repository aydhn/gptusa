from datetime import datetime, timezone
from typing import Any
from usa_signal_bot.core.enums import ShadowSessionStatus, ShadowRuntimeMode
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowPortfolioState,
    ShadowSignal,
    ShadowOrderIntent,
    ShadowFill,
    ShadowPnLSnapshot,
    ShadowRehearsalSession,
    create_shadow_rehearsal_session_id
)
from usa_signal_bot.paper_shadow.shadow_safety_guard import assert_shadow_session_safe, ShadowSafetyError

class PaperShadowRehearsalRunner:
    def __init__(self, runtime_mode: ShadowRuntimeMode = ShadowRuntimeMode.FULL_PAPER_SHADOW):
        self.runtime_mode = runtime_mode

    def run_rehearsal(self, context: ShadowSimulationContext) -> ShadowRehearsalSession:
        from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
        from usa_signal_bot.paper_shadow.shadow_ledger import build_ledger_from_shadow_session

        session = ShadowRehearsalSession(
            session_id=create_shadow_rehearsal_session_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=ShadowSessionStatus.RUNNING,
            signals=[],
            order_intents=[],
            fills=[],
            ledger_events=[],
            pnl_snapshots=[],
            safety_flags=[],
            output_paths={},
            warnings=[],
            errors=[],
            context=context,
            started_at_utc=datetime.now(timezone.utc).isoformat()
        )
        try:
            assert_shadow_session_safe(context)

            if self.runtime_mode in [ShadowRuntimeMode.PORTFOLIO_SHADOW, ShadowRuntimeMode.FULL_PAPER_SHADOW]:
                portfolio = self.run_portfolio_init_stage(context)
                session.portfolio_state = portfolio

            signals = self.run_signal_stage(context)
            session.signals = signals

            candidates = self.run_candidate_stage(signals)

            if self.runtime_mode in [ShadowRuntimeMode.PORTFOLIO_SHADOW, ShadowRuntimeMode.FULL_PAPER_SHADOW]:
                intents = self.run_intent_stage(candidates)
                intents = self.run_risk_stage(intents, session.portfolio_state, context)
                session.order_intents = intents

                assert_shadow_session_safe(context, intents)

                fills = self.run_fill_stage(intents)
                session.fills = fills

                assert_shadow_session_safe(context, intents, fills)

                session.portfolio_state = self.run_portfolio_stage(session.portfolio_state, fills)
                pnl = self.run_pnl_stage(session.portfolio_state, fills, context.starting_equity_usd)
                session.pnl_snapshots.append(pnl)

            session.status = ShadowSessionStatus.COMPLETED

        except ShadowSafetyError as e:
            session.status = ShadowSessionStatus.BLOCKED
            session.errors.append(str(e))
        except Exception as e:
            session.status = ShadowSessionStatus.FAILED
            session.errors.append(str(e))
        finally:
            session.completed_at_utc = datetime.now(timezone.utc).isoformat()
            session.ledger_events = build_ledger_from_shadow_session(session)

        return session

    def run_portfolio_init_stage(self, context: ShadowSimulationContext) -> ShadowPortfolioState:
        from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
        return initialize_shadow_portfolio(context)

    def run_signal_stage(self, context: ShadowSimulationContext) -> list[ShadowSignal]:
        from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_shadow_signals
        return generate_shadow_signals(context)

    def run_candidate_stage(self, signals: list[ShadowSignal]) -> list[ShadowSignal]:
        from usa_signal_bot.paper_shadow.shadow_candidate_selection import select_shadow_candidates
        return select_shadow_candidates(signals)

    def run_intent_stage(self, candidates: list[ShadowSignal]) -> list[ShadowOrderIntent]:
        from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents, block_real_order_like_intents
        intents = build_shadow_order_intents(candidates)
        return block_real_order_like_intents(intents)

    def run_risk_stage(self, intents: list[ShadowOrderIntent], portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> list[ShadowOrderIntent]:
        from usa_signal_bot.paper_shadow.shadow_risk_gate import apply_shadow_risk_gates
        return apply_shadow_risk_gates(intents, portfolio, context)

    def run_fill_stage(self, intents: list[ShadowOrderIntent]) -> list[ShadowFill]:
        from usa_signal_bot.paper_shadow.shadow_fill_simulator import simulate_shadow_fills
        return simulate_shadow_fills(intents)

    def run_portfolio_stage(self, portfolio: ShadowPortfolioState, fills: list[ShadowFill]) -> ShadowPortfolioState:
        from usa_signal_bot.paper_shadow.shadow_portfolio import update_shadow_portfolio_with_fill
        for fill in fills:
            portfolio = update_shadow_portfolio_with_fill(portfolio, fill)
        return portfolio

    def run_pnl_stage(self, portfolio: ShadowPortfolioState, fills: list[ShadowFill], starting_equity_usd: float) -> ShadowPnLSnapshot:
        from usa_signal_bot.paper_shadow.shadow_pnl_tracker import update_shadow_pnl_after_fills
        return update_shadow_pnl_after_fills(portfolio, fills, starting_equity_usd)

    def run_rebalance_stage(self, portfolio: ShadowPortfolioState, context: ShadowSimulationContext) -> dict[str, Any]:
        from usa_signal_bot.paper_shadow.shadow_rebalance import build_shadow_rebalance_preview
        return build_shadow_rebalance_preview(portfolio, context)

    def run_notification_stage(self, session: ShadowRehearsalSession) -> dict[str, Any]:
        from usa_signal_bot.paper_shadow.shadow_notifications import build_shadow_notification_preview
        return build_shadow_notification_preview(session)
