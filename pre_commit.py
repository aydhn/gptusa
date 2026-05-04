import subprocess
import sys

def run_tests():
    print("Running tests...")
    subprocess.check_call([sys.executable, "-m", "pytest", "tests/"])
    print("Tests passed.")

def run_smoke():
    print("Running smoke test...")
    subprocess.check_call([sys.executable, "-m", "usa_signal_bot", "smoke"])
    print("Smoke test passed.")

if __name__ == "__main__":
    try:
        run_tests()
        run_smoke()
        print("Pre-commit passed.")
        sys.exit(0)
    except subprocess.CalledProcessError:
        print("Pre-commit failed.")
        sys.exit(1)
