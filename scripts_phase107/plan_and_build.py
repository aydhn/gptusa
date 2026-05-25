import os
import subprocess

print("Continuing the building of phase 107 models and folders")

# Let's create the directories
dirs = [
    "usa_signal_bot/data_provider_runtime",
    "tests/fixtures/providers",
]
for d in dirs:
    os.makedirs(d, exist_ok=True)
