def fix():
    with open("usa_signal_bot/backtesting/allocation_drift.py", "r") as f:
        content = f.read()

    new_fn = """
def calculate_target_weights_from_replay_items(items) -> dict:
    return {}
"""
    if "calculate_target_weights_from_replay_items" not in content:
        content = content + "\n" + new_fn

    with open("usa_signal_bot/backtesting/allocation_drift.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix()
