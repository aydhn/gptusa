import pytest
from usa_signal_bot.core.enums import AttributionDimension, ContributionDirection
from usa_signal_bot.attribution.attribution_models import AttributionContribution
from usa_signal_bot.attribution.attribution_ranking import rank_contributions_by_net_pnl, rank_contributions_by_cost_drag

def _get_mock_contribs():
    return [
        AttributionContribution(contribution_id="c1", dimension=AttributionDimension.SYMBOL, name="AAPL", contribution_direction=ContributionDirection.POSITIVE, gross_pnl_usd=100, net_pnl_usd=90, total_cost_usd=10, trade_count=1, win_count=1, loss_count=0),
        AttributionContribution(contribution_id="c2", dimension=AttributionDimension.SYMBOL, name="MSFT", contribution_direction=ContributionDirection.NEGATIVE, gross_pnl_usd=20, net_pnl_usd=-10, total_cost_usd=30, trade_count=1, win_count=0, loss_count=1),
    ]

def test_rank_contributions_by_net_pnl():
    contribs = _get_mock_contribs()
    ranked = rank_contributions_by_net_pnl(contribs)
    assert ranked[0].name == "AAPL"

    ranked_asc = rank_contributions_by_net_pnl(contribs, descending=False)
    assert ranked_asc[0].name == "MSFT"

def test_rank_contributions_by_cost_drag():
    contribs = _get_mock_contribs()
    ranked = rank_contributions_by_cost_drag(contribs)
    assert ranked[0].name == "MSFT" # 30/20 = 150% drag vs 10/100 = 10% drag
