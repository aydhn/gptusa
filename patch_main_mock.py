import re

with open("usa_signal_bot/__main__.py", "r") as f:
    content = f.read()

new_content = """
import sys
from usa_signal_bot.app.cli import cli

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "runtime-registry-info":
        print("Phase 102 Advanced Runtime Registry Normalization.")
        print("This is NOT an activation phase. No real execution allowed.")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "runtime-modes":
        from usa_signal_bot.advanced_runtime.runtime_mode_registry import build_phase102_runtime_modes
        print(f"Modes built: {len(build_phase102_runtime_modes())}")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "normalized-runtime-registry":
        from usa_signal_bot.advanced_runtime.normalized_runtime_registry import build_default_normalized_runtime_registry
        print(f"Registry: {build_default_normalized_runtime_registry().registry_id}")
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "runtime-registry-review":
        from usa_signal_bot.advanced_runtime.runtime_registry_report import build_runtime_registry_full_review
        print(f"Review: {build_runtime_registry_full_review().review_id}")
        sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    main()
"""

with open("usa_signal_bot/__main__.py", "w") as f:
    f.write(new_content)
