with open("usa_signal_bot/paper_observation/dry_run_ingestion.py", "r") as f:
    code = f.read()

code = code.replace(
    'if payload.get("blocked_operation_count", 0) > 0:',
    'if len([e for e in extract_bridge_telemetry_events(payload) if e.get("event_type") == "BLOCKED_OPERATION"]) > 0 or payload.get("blocked_operation_count", 0) > 0:'
)

with open("usa_signal_bot/paper_observation/dry_run_ingestion.py", "w") as f:
    f.write(code)
