with open("usa_signal_bot/notifications/notification_templates.py", "r") as f:
    content = f.read()

new_templates = """
def format_feature_enrichment_report_message(review: Any) -> Any:
    return {"subject": "Feature Enrichment Review", "body": "Phase 119 completed.", "risk_flags": []}

def format_feature_interaction_warning_message(result: Any) -> Any:
    return {"subject": "Feature Interaction Warning", "body": "Check interaction schema.", "risk_flags": []}

def format_enriched_feature_table_warning_message(tables: list[Any]) -> Any:
    return {"subject": "Enriched Feature Table Warning", "body": "Check table schema.", "risk_flags": []}

def notifications_from_feature_enrichment_review(review: Any) -> list[Any]:
    return [format_feature_enrichment_report_message(review)]
"""

if "format_feature_enrichment_report_message" not in content:
    content += "\nfrom typing import Any\n" + new_templates
    with open("usa_signal_bot/notifications/notification_templates.py", "w") as f:
        f.write(content)
    print("Updated notification_templates.py")
