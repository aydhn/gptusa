import sys
from pathlib import Path
from usa_signal_bot.release.backup_restore import create_backup_request, build_backup, backup_result_to_text
from usa_signal_bot.core.enums import BackupScope
from usa_signal_bot.core.config import load_app_config

def main():
    cfg = load_app_config()
    request = create_backup_request(BackupScope("CONFIG_ONLY"), cfg.backup.output_dir)
    result = build_backup(Path("."), Path("data"), request)
    print(backup_result_to_text(result))

if __name__ == "__main__":
    main()
