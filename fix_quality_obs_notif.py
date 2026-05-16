import os

# quality
q_path = "usa_signal_bot/quality/data_quality_evaluator.py"
with open(q_path, "r") as f:
    q_content = f.read()

new_q = """
def update_quality_scorecard_with_portfolio(scorecard: dict, plan) -> dict:
    res = dict(scorecard)
    res["portfolio_construction_quality_score"] = 100.0 if not plan.conflicts else 80.0
    if plan.blocked_count > 0:
        res["portfolio_guard_score"] = max(0.0, 100.0 - (plan.blocked_count * 10.0))
    else:
        res["portfolio_guard_score"] = 100.0
    return res
"""
if "update_quality_scorecard_with_portfolio" not in q_content:
    with open(q_path, "a") as f:
        f.write(new_q)

# obs
o_path = "usa_signal_bot/observability/metrics_collector.py"
with open(o_path, "r") as f:
    o_content = f.read()

new_o = """
def collect_portfolio_metrics(plan) -> dict:
    m = {}
    if plan.exposure_snapshot:
        m["latest_portfolio_gross_exposure_usd"] = plan.exposure_snapshot.gross_exposure_usd
        m["latest_portfolio_net_exposure_usd"] = plan.exposure_snapshot.net_exposure_usd
        m["latest_portfolio_long_exposure_usd"] = plan.exposure_snapshot.long_exposure_usd
        m["latest_portfolio_short_exposure_usd"] = plan.exposure_snapshot.short_exposure_usd
    m["latest_portfolio_blocked_allocation_count"] = plan.blocked_count + plan.suppressed_count
    m["portfolio_construction_warning_count"] = len(plan.warnings)
    return m
"""
if "collect_portfolio_metrics" not in o_content:
    with open(o_path, "a") as f:
        f.write(new_o)

# notif
n_path = "usa_signal_bot/notifications/notification_templates.py"
with open(n_path, "r") as f:
    n_content = f.read()

new_n = """
def format_portfolio_construction_report_message(review) -> dict:
    from usa_signal_bot.portfolio_construction.construction_reporting import portfolio_construction_review_to_text
    return {
        "title": "Portfolio Construction Review",
        "body": portfolio_construction_review_to_text(review, 10)
    }

def notifications_from_portfolio_construction_review(review) -> list:
    return [format_portfolio_construction_report_message(review)]
"""
if "format_portfolio_construction_report_message" not in n_content:
    with open(n_path, "a") as f:
        f.write(new_n)
