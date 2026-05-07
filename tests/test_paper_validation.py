import pytest
from usa_signal_bot.paper.paper_validation import (
    validate_paper_engine_config, validate_paper_order_intent_report,
    validate_no_broker_execution_in_paper, validate_no_live_order_language_in_paper,
    assert_paper_valid
)
from usa_signal_bot.paper.paper_engine import PaperEngineConfig
from usa_signal_bot.paper.paper_models import PaperOrderIntent, PaperEngineRunResult, VirtualAccount
from usa_signal_bot.core.enums import PaperExecutionMode, PaperOrderSide, PaperOrderType, PaperAccountStatus, PaperEngineStatus
from usa_signal_bot.core.exceptions import PaperValidationError

def test_validate_paper_config():
    cfg = PaperEngineConfig(
        execution_mode=PaperExecutionMode.DRY_RUN,
        starting_cash=10000.0,
        fee_bps=1.0,
        slippage_bps=2.0,
        allow_fractional_quantity=True,
        allow_short=True, # Will cause warning
        max_positions=20,
        max_order_notional=10000.0,
        max_total_exposure_pct=0.8,
        reject_duplicate_symbol_position=True,
        write_outputs=False
    )

    rep = validate_paper_engine_config(cfg)
    assert rep.valid is True
    assert rep.warning_count == 1 # allow_short
    assert rep.error_count == 0

def test_validate_paper_intent():
    intent = PaperOrderIntent(
        order_id="i1",
        source="SIGNAL",
        source_id=None,
        symbol="", # invalid
        timeframe="1d",
        side=PaperOrderSide.BUY,
        order_type=PaperOrderType.MARKET,
        quantity=0, # invalid
        notional=None,
        created_at_utc=""
    )

    rep = validate_paper_order_intent_report(intent)
    assert rep.valid is False
    assert rep.error_count == 2

def test_no_broker_execution_leak():
    # Construct a dummy run result
    acct = VirtualAccount(
        account_id="a1", name="test", status=PaperAccountStatus.ACTIVE,
        starting_cash=1000, cash=1000, equity=1000, realized_pnl=0, unrealized_pnl=0,
        created_at_utc="now", metadata={"broker_order": "1234"} # The leak
    )

    res = PaperEngineRunResult(
        run_id="r1", created_at_utc="now", status=PaperEngineStatus.COMPLETED,
        account=acct, orders=[], fills=[], positions=[], cash_ledger=[],
        equity_snapshots=[], trades=[], output_paths={}, warnings=[], errors=[]
    )

    rep = validate_no_broker_execution_in_paper(res)
    assert rep.valid is False

    with pytest.raises(PaperValidationError):
        assert_paper_valid(rep)

def test_no_live_language_leak():
    acct = VirtualAccount(
        account_id="a1", name="test", status=PaperAccountStatus.ACTIVE,
        starting_cash=1000, cash=1000, equity=1000, realized_pnl=0, unrealized_pnl=0,
        created_at_utc="now", metadata={"note": "sent to broker"} # The leak
    )

    res = PaperEngineRunResult(
        run_id="r1", created_at_utc="now", status=PaperEngineStatus.COMPLETED,
        account=acct, orders=[], fills=[], positions=[], cash_ledger=[],
        equity_snapshots=[], trades=[], output_paths={}, warnings=[], errors=[]
    )

    rep = validate_no_live_order_language_in_paper(res)
    assert rep.valid is False
