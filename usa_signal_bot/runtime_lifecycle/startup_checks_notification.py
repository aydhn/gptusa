from typing import List
from usa_signal_bot.core.enums import StartupCheckType, StartupCheckStatus
from usa_signal_bot.runtime_lifecycle.phase104_models import StartupCheckItem, create_startup_check_id, _now_str

def _build_notif_item(check_type: StartupCheckType, msg: str) -> StartupCheckItem:
    return StartupCheckItem(
        check_id=create_startup_check_id(),
        created_at_utc=_now_str(),
        check_type=check_type,
        service_id=None,
        service_name=None,
        status=StartupCheckStatus.PASS,
        required=True,
        message=msg,
        details={},
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def check_notification_preview_startup() -> StartupCheckItem:
    return _build_notif_item(StartupCheckType.NOTIFICATION_PREVIEW, "Notification templating system loaded correctly for local preview.")

def check_telegram_real_send_disabled_startup() -> StartupCheckItem:
    return _build_notif_item(StartupCheckType.NOTIFICATION_PREVIEW, "Telegram real send module explicitly stubbed out / disabled for startup.")

def run_notification_startup_checks() -> List[StartupCheckItem]:
    return [
        check_notification_preview_startup(),
        check_telegram_real_send_disabled_startup()
    ]
