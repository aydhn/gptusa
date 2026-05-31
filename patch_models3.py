with open("usa_signal_bot/regime_classification/freeze_preparation/phase134_models.py", "r") as f:
    text = f.read()

# Let's see what is overriding field
lines = text.split("\n")
for i, line in enumerate(lines):
    if "field =" in line or "field=" in line:
        print(f"Line {i+1}: {line}")
