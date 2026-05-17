import pytest
import subprocess

def run_cmd(cmd):
    return subprocess.run(["python", "-m", "usa_signal_bot"] + cmd, capture_options=True, text=True)

# For speed, we just use a small script that tests the routing to avoid full python startup overhead
# But since this is a requirement, let's just make sure the command is registered without crashing.
