import datetime
from typing import Any, List, Optional
import statistics

from usa_signal_bot.core.enums import LiquidityStatus, LiquidityMetricName
from usa_signal_bot.execution.liquidity_models import (
    LiquidityProfile,
    LiquidityMetric,
    create_liquidity_profile_id,
    create_liquidity_metric_id,
    validate_liquidity_profile
)
from usa_signal_bot.core.config_schema import LiquidityGuardConfig

def calculate_avg_daily_volume(rows: list[dict[str, Any]], lookback_bars: int = 60) -> float | None:
    if not rows:
        return None
    recent_rows = rows[-lookback_bars:]
    volumes = [r.get("volume", 0) for r in recent_rows if r.get("volume") is not None]
    if not volumes:
        return None
    return sum(volumes) / len(volumes)

def calculate_avg_dollar_volume(rows: list[dict[str, Any]], lookback_bars: int = 60) -> float | None:
    if not rows:
        return None
    recent_rows = rows[-lookback_bars:]
    dollar_volumes = []
    for r in recent_rows:
        c = r.get("close")
        v = r.get("volume")
        if c is not None and v is not None:
            dollar_volumes.append(c * v)
    if not dollar_volumes:
        return None
    return sum(dollar_volumes) / len(dollar_volumes)

def calculate_median_daily_volume(rows: list[dict[str, Any]], lookback_bars: int = 60) -> float | None:
    if not rows:
        return None
    recent_rows = rows[-lookback_bars:]
    volumes = [r.get("volume", 0) for r in recent_rows if r.get("volume") is not None]
    if not volumes:
        return None
    return statistics.median(volumes)

def calculate_median_dollar_volume(rows: list[dict[str, Any]], lookback_bars: int = 60) -> float | None:
    if not rows:
        return None
    recent_rows = rows[-lookback_bars:]
    dollar_volumes = []
    for r in recent_rows:
        c = r.get("close")
        v = r.get("volume")
        if c is not None and v is not None:
            dollar_volumes.append(c * v)
    if not dollar_volumes:
        return None
    return statistics.median(dollar_volumes)

def calculate_atr_pct(rows: list[dict[str, Any]], lookback_bars: int = 14) -> float | None:
    if len(rows) < lookback_bars + 1:
        return None

    recent_rows = rows[-(lookback_bars+1):]
    tr_list = []
    for i in range(1, len(recent_rows)):
        high = recent_rows[i].get("high")
        low = recent_rows[i].get("low")
        prev_close = recent_rows[i-1].get("close")
        if high is None or low is None or prev_close is None:
            continue
        tr1 = high - low
        tr2 = abs(high - prev_close)
        tr3 = abs(low - prev_close)
        tr_list.append(max(tr1, tr2, tr3))

    if not tr_list:
        return None

    atr = sum(tr_list) / len(tr_list)
    last_close = recent_rows[-1].get("close")

    if last_close is None or last_close == 0:
        return None

    return (atr / last_close) * 100.0

def calculate_last_gap_pct(rows: list[dict[str, Any]]) -> float | None:
    if len(rows) < 2:
        return None

    last_row = rows[-1]
    prev_row = rows[-2]

    curr_open = last_row.get("open")
    prev_close = prev_row.get("close")

    if curr_open is None or prev_close is None or prev_close == 0:
        return None

    return abs(curr_open - prev_close) / prev_close * 100.0

def calculate_stale_data_days(rows: list[dict[str, Any]], today: str | None = None) -> int | None:
    if not rows:
        return None

    last_row = rows[-1]
    date_str = last_row.get("date")
    if not date_str:
        return None

    try:
        last_date = datetime.datetime.fromisoformat(date_str).date()
        if today:
            ref_date = datetime.datetime.fromisoformat(today).date()
        else:
            ref_date = datetime.datetime.utcnow().date()

        diff = (ref_date - last_date).days
        return max(0, diff)
    except Exception:
        return None

def classify_liquidity_status(profile: LiquidityProfile, config: LiquidityGuardConfig = None) -> LiquidityStatus:
    if config is None:
        config = LiquidityGuardConfig()

    if profile.avg_daily_volume is None or profile.avg_dollar_volume is None:
        return LiquidityStatus.INSUFFICIENT_DATA

    adv = profile.avg_daily_volume
    addv = profile.avg_dollar_volume

    if adv >= config.min_avg_daily_volume * 10 and addv >= config.min_avg_dollar_volume * 10:
        return LiquidityStatus.EXCELLENT

    if adv >= config.min_avg_daily_volume * 2 and addv >= config.min_avg_dollar_volume * 2:
        return LiquidityStatus.GOOD

    if adv >= config.min_avg_daily_volume and addv >= config.min_avg_dollar_volume:
        return LiquidityStatus.ACCEPTABLE

    if adv >= config.thin_avg_daily_volume and addv >= config.thin_avg_dollar_volume:
        return LiquidityStatus.THIN

    return LiquidityStatus.ILLIQUID

def calculate_liquidity_profile(symbol: str, rows: list[dict[str, Any]], lookback_bars: int = 60, config: LiquidityGuardConfig = None) -> LiquidityProfile:
    if config is None:
        config = LiquidityGuardConfig()

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    adv = calculate_avg_daily_volume(rows, lookback_bars)
    addv = calculate_avg_dollar_volume(rows, lookback_bars)
    mdv = calculate_median_daily_volume(rows, lookback_bars)
    mddv = calculate_median_dollar_volume(rows, lookback_bars)
    atr = calculate_atr_pct(rows, 14)
    gap = calculate_last_gap_pct(rows)
    stale = calculate_stale_data_days(rows)

    last_price = rows[-1].get("close") if rows else None
    last_volume = rows[-1].get("volume") if rows else None

    metrics = []

    def add_metric(name, value, unit=None):
        if value is not None:
            metrics.append(LiquidityMetric(
                metric_id=create_liquidity_metric_id(symbol, name),
                symbol=symbol,
                metric_name=name,
                value=value,
                unit=unit,
                created_at_utc=now_utc,
                lookback_bars=lookback_bars
            ))

    add_metric(LiquidityMetricName.AVG_DAILY_VOLUME, adv, "shares")
    add_metric(LiquidityMetricName.AVG_DOLLAR_VOLUME, addv, "USD")
    add_metric(LiquidityMetricName.MEDIAN_DAILY_VOLUME, mdv, "shares")
    add_metric(LiquidityMetricName.MEDIAN_DOLLAR_VOLUME, mddv, "USD")
    add_metric(LiquidityMetricName.ATR_PCT, atr, "pct")
    add_metric(LiquidityMetricName.GAP_PCT, gap, "pct")
    add_metric(LiquidityMetricName.STALE_DATA_DAYS, stale, "days")
    add_metric(LiquidityMetricName.LAST_VOLUME, last_volume, "shares")
    add_metric(LiquidityMetricName.PRICE_LEVEL, last_price, "USD")

    profile = LiquidityProfile(
        profile_id=create_liquidity_profile_id(symbol),
        symbol=symbol,
        created_at_utc=now_utc,
        status=LiquidityStatus.UNKNOWN,
        avg_daily_volume=adv,
        avg_dollar_volume=addv,
        median_daily_volume=mdv,
        median_dollar_volume=mddv,
        last_price=last_price,
        last_volume=last_volume,
        atr_pct=atr,
        gap_pct=gap,
        stale_data_days=stale,
        metrics=metrics,
        warnings=[],
        errors=[],
        metadata={}
    )

    profile.status = classify_liquidity_status(profile, config)

    if profile.status == LiquidityStatus.INSUFFICIENT_DATA:
        profile.warnings.append("Insufficient data to classify liquidity.")
    elif profile.status == LiquidityStatus.ILLIQUID:
        profile.warnings.append("Symbol is classified as ILLIQUID.")
    elif profile.status == LiquidityStatus.THIN:
        profile.warnings.append("Symbol has THIN liquidity.")

    if stale is not None and stale > config.max_stale_days:
        profile.warnings.append(f"Data is stale by {stale} days.")

    validate_liquidity_profile(profile)
    return profile

def liquidity_profile_to_text(profile: LiquidityProfile) -> str:
    lines = [
        f"Liquidity Profile for {profile.symbol}:",
        f"  Status: {profile.status.value}",
        f"  Last Price: {profile.last_price}",
        f"  ADV: {profile.avg_daily_volume}",
        f"  ADDV: {profile.avg_dollar_volume}",
        f"  ATR Pct: {profile.atr_pct}%",
        f"  Stale Days: {profile.stale_data_days}"
    ]
    if profile.warnings:
        lines.append("  Warnings:")
        for w in profile.warnings:
            lines.append(f"   - {w}")

    lines.append("  Note: Liquidity metrics are proxies and do not represent investment advice.")
    return "\n".join(lines)
