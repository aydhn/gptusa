from datetime import datetime, date, timedelta
from pathlib import Path
from usa_signal_bot.core.enums import WalkForwardMode, WalkForwardWindowStatus
from usa_signal_bot.backtesting.walk_forward_models import WalkForwardConfig, WalkForwardWindow
from usa_signal_bot.data.cache import find_latest_cache_file, read_cached_ohlcv_bars

def default_walk_forward_config() -> WalkForwardConfig:
    return WalkForwardConfig(
        mode=WalkForwardMode.ROLLING,
        train_window_days=365,
        test_window_days=90,
        step_days=90,
        min_train_days=180,
        max_windows=20,
        anchored_start=False,
        include_partial_last_window=False
    )

def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()

def date_to_str(value: date) -> str:
    return value.strftime("%Y-%m-%d")

def generate_walk_forward_windows(start_date: str, end_date: str, config: WalkForwardConfig | None = None) -> list[WalkForwardWindow]:
    if not config:
        config = default_walk_forward_config()

    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)

    if start_dt >= end_dt:
        raise ValueError(f"start_date ({start_date}) must be before end_date ({end_date})")

    if config.mode == WalkForwardMode.ROLLING:
        return generate_rolling_windows(
            start_date,
            end_date,
            config.train_window_days,
            config.test_window_days,
            config.step_days,
            config.max_windows,
            config.include_partial_last_window
        )
    elif config.mode == WalkForwardMode.ANCHORED:
        return generate_anchored_windows(
            start_date,
            end_date,
            config.min_train_days,
            config.test_window_days,
            config.step_days,
            config.max_windows,
            config.include_partial_last_window
        )
    elif config.mode == WalkForwardMode.EXPANDING:
         return generate_expanding_windows(
            start_date,
            end_date,
            config.min_train_days,
            config.test_window_days,
            config.step_days,
            config.max_windows,
            config.include_partial_last_window
        )
    else:
        raise ValueError(f"Unsupported WalkForwardMode: {config.mode}")

def generate_rolling_windows(
    start_date: str,
    end_date: str,
    train_window_days: int,
    test_window_days: int,
    step_days: int,
    max_windows: int,
    include_partial_last_window: bool = False
) -> list[WalkForwardWindow]:

    windows = []
    current_train_start = parse_date(start_date)
    end_dt = parse_date(end_date)
    index = 1

    while index <= max_windows:
        current_train_end = current_train_start + timedelta(days=train_window_days)
        current_test_start = current_train_end
        current_test_end = current_test_start + timedelta(days=test_window_days)

        # Check boundaries
        if current_train_end >= end_dt:
            break

        is_partial = current_test_end > end_dt

        if is_partial:
            if not include_partial_last_window:
                break
            current_test_end = end_dt

        if current_test_start >= current_test_end:
            break

        windows.append(WalkForwardWindow(
            window_id=f"win_{index:03d}",
            index=index,
            mode=WalkForwardMode.ROLLING,
            train_start=date_to_str(current_train_start),
            train_end=date_to_str(current_train_end),
            test_start=date_to_str(current_test_start),
            test_end=date_to_str(current_test_end),
            full_start=date_to_str(current_train_start),
            full_end=date_to_str(current_test_end),
            status=WalkForwardWindowStatus.CREATED,
            metadata={"is_partial": is_partial}
        ))

        if is_partial:
            break

        current_train_start += timedelta(days=step_days)
        index += 1

    return windows

def generate_anchored_windows(
    start_date: str,
    end_date: str,
    min_train_days: int,
    test_window_days: int,
    step_days: int,
    max_windows: int,
    include_partial_last_window: bool = False
) -> list[WalkForwardWindow]:

    windows = []
    train_start = parse_date(start_date)
    end_dt = parse_date(end_date)
    index = 1

    current_train_end = train_start + timedelta(days=min_train_days)

    while index <= max_windows:
        current_test_start = current_train_end
        current_test_end = current_test_start + timedelta(days=test_window_days)

        if current_train_end >= end_dt:
            break

        is_partial = current_test_end > end_dt

        if is_partial:
            if not include_partial_last_window:
                break
            current_test_end = end_dt

        if current_test_start >= current_test_end:
            break

        windows.append(WalkForwardWindow(
            window_id=f"win_{index:03d}",
            index=index,
            mode=WalkForwardMode.ANCHORED,
            train_start=date_to_str(train_start),
            train_end=date_to_str(current_train_end),
            test_start=date_to_str(current_test_start),
            test_end=date_to_str(current_test_end),
            full_start=date_to_str(train_start),
            full_end=date_to_str(current_test_end),
            status=WalkForwardWindowStatus.CREATED,
            metadata={"is_partial": is_partial}
        ))

        if is_partial:
            break

        current_train_end += timedelta(days=step_days)
        index += 1

    return windows

def generate_expanding_windows(
    start_date: str,
    end_date: str,
    min_train_days: int,
    test_window_days: int,
    step_days: int,
    max_windows: int,
    include_partial_last_window: bool = False
) -> list[WalkForwardWindow]:
    # In many systems expanding and anchored are synonyms for walk-forward,
    # but we map it to anchored logic here as defined by the user requirements (min_train_days start expanding).
    windows = generate_anchored_windows(start_date, end_date, min_train_days, test_window_days, step_days, max_windows, include_partial_last_window)
    for w in windows:
        w.mode = WalkForwardMode.EXPANDING
    return windows

def split_window_dates(window: WalkForwardWindow) -> dict[str, tuple[str, str]]:
    return {
        "train": (window.train_start, window.train_end),
        "test": (window.test_start, window.test_end),
        "full": (window.full_start, window.full_end)
    }

def infer_date_range_from_cached_bars(data_root: Path, symbols: list[str], timeframe: str, provider_name: str = "yfinance") -> tuple[str | None, str | None, list[str]]:
    warnings = []
    earliest_date = None
    latest_date = None

    for symbol in symbols:
        try:
            cache_path = find_latest_cache_file(data_root, provider_name, symbol, timeframe)
            bars = read_cached_ohlcv_bars(cache_path) if cache_path else []
            if not bars:
                warnings.append(f"No cached bars found for {symbol}")
                continue

            first_dt = bars[0].timestamp_utc[:10]  # Take YYYY-MM-DD
            last_dt = bars[-1].timestamp_utc[:10]

            if earliest_date is None or first_dt < earliest_date:
                earliest_date = first_dt
            if latest_date is None or last_dt > latest_date:
                latest_date = last_dt
        except Exception as e:
            warnings.append(f"Error loading cache for {symbol}: {e}")

    return earliest_date, latest_date, warnings
