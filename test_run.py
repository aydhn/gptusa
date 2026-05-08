from usa_signal_bot.release.maintenance_tasks import default_maintenance_plan, maintenance_plan_to_markdown
plan = default_maintenance_plan()
print(maintenance_plan_to_markdown(plan))
