import sys
from pathlib import Path
from usa_signal_bot.release.local_packager import LocalReleasePackager
from usa_signal_bot.release.release_models import ReleaseBuildRequest
from usa_signal_bot.core.config import load_app_config

def main():
    cfg = load_app_config()
    packager = LocalReleasePackager(project_root=Path("."), data_root=Path("data"))
    request = ReleaseBuildRequest(
        request_id="test",
        release_name=cfg.release.release_name,
        output_dir=cfg.release.output_dir,
        include_tests=True,
        include_reports=False,
        include_data_cache=False,
        include_secrets=False
    )
    result = packager.build(request)
    print(f"Status: {result.status.value}")
    if result.errors:
        for err in result.errors:
            print(f"Error: {err}")
    if result.bundle_path:
        print(f"Written release build to {result.bundle_path}")

if __name__ == "__main__":
    main()
