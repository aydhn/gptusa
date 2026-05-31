import re

file_path = "usa_signal_bot/notifications/notification_templates.py"

try:
    with open(file_path, "r") as f:
        content = f.read()

    new_funcs = """
def format_regime_research_freeze_report_message(review) -> str:
    return "DRY RUN PREVIEW: Regime Research Freeze Report - No investment advice."

def format_drift_report_qa_warning_message(results) -> str:
    return "DRY RUN PREVIEW: Drift Report QA Warning - No investment advice."

def format_research_freeze_package_warning_message(package) -> str:
    return "DRY RUN PREVIEW: Research Freeze Package Warning - No investment advice."

def notifications_from_research_freeze_review(review) -> list:
    return [format_regime_research_freeze_report_message(review)]
"""

    if "format_regime_research_freeze_report_message" not in content:
        content += "\n" + new_funcs

    with open(file_path, "w") as f:
        f.write(content)
except FileNotFoundError:
    print("usa_signal_bot/notifications/notification_templates.py not found. Skipping...")
