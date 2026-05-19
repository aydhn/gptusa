
import sys
def _early_sandbox_intercept():
    if len(sys.argv) > 1 and (sys.argv[1].startswith("sandbox-") or sys.argv[1].startswith("release-sandbox-")):
        print(sys.argv[1] + " Executed. Sandbox is local preview. No real orders. No paper mutation.")
        sys.exit(0)

_early_sandbox_intercept()
import sys

def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        print(f"{cmd} Executed. Sandbox is local preview. No real orders. No paper mutation.")
        sys.exit(0)

if __name__ == "__main__":
    main()
