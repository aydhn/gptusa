"""Runner script for smoke tests."""

import sys
import subprocess

def run_smoke():
    print("Running Smoke Tests...")

    # 1. Test CLI execution
    print("\n--- CLI Smoke Command ---")
    try:
        subprocess.run([sys.executable, "-m", "usa_signal_bot", "smoke"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"CLI Smoke test failed: {e}")
        return 1

    # 2. Test CLI show-config
    print("\n--- CLI Show Config Command ---")
    try:
        subprocess.run([sys.executable, "-m", "usa_signal_bot", "show-config"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"CLI Show Config test failed: {e}")
        return 1

    # 3. Test CLI show-paths
    print("\n--- CLI Show Paths Command ---")
    try:
        subprocess.run([sys.executable, "-m", "usa_signal_bot", "show-paths"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"CLI Show Paths test failed: {e}")
        return 1

    print("\nAll scripts smoke tests passed successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(run_smoke())
