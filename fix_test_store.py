with open("usa_signal_bot/paper_observation/observation_store.py", "r") as f:
    code = f.read()

# Add missing 'import os' if not exists
if "import os" not in code:
    code = "import os\n" + code

with open("usa_signal_bot/paper_observation/observation_store.py", "w") as f:
    f.write(code)
