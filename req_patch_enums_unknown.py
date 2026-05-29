with open("usa_signal_bot/core/enums.py", "r") as f:
    content = f.read()

content = content.replace("FULL_PHASE130_REVIEW = \"FULL_PHASE130_REVIEW\"", "FULL_PHASE130_REVIEW = \"FULL_PHASE130_REVIEW\"\n    UNKNOWN = \"UNKNOWN\"")

with open("usa_signal_bot/core/enums.py", "w") as f:
    f.write(content)
