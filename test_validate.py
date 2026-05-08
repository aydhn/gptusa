import sys
from pathlib import Path
from usa_signal_bot.release.release_store import get_latest_release_build_dir
from usa_signal_bot.release.release_validation import validate_release_bundle_file
from usa_signal_bot.core.config import load_app_config

def main():
    cfg = load_app_config()
    dirs = list(Path("data/release/builds").iterdir())
    latest_dir = dirs[0]
    bundle_path = latest_dir / f"{cfg.release.release_name}.zip"

    print(f"Validating bundle: {bundle_path}")

    report = validate_release_bundle_file(Path(bundle_path))
    print(f"Valid: {report.valid}")
    if not report.valid:
        for err in report.errors:
            print(f"Error: {err}")

if __name__ == "__main__":
    main()
