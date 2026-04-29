from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
from usa_signal_bot.core.enums import CacheDecision
from usa_signal_bot.data.downloader import MarketDataDownloader
from usa_signal_bot.data.models import MarketDataRequest

@dataclass
class CacheRefreshRequest:
    provider_name: str
    symbols: List[str]
    timeframe: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    force_refresh: bool = False
    use_cache: bool = True

@dataclass
class CacheFileStatus:
    symbol: str
    cache_path: str
    exists: bool
    is_fresh: bool
    age_seconds: Optional[float]
    size_bytes: Optional[int]
    decision: CacheDecision
    reason: str

@dataclass
class CacheRefreshPlan:
    request: CacheRefreshRequest
    created_at_utc: str
    statuses: List[CacheFileStatus]
    symbols_to_refresh: List[str]
    symbols_from_cache: List[str]
    estimated_requests: int

@dataclass
class CacheRefreshResult:
    plan: CacheRefreshPlan
    refreshed_symbols: List[str]
    cache_used_symbols: List[str]
    failed_symbols: List[str]
    errors: List[str]
    warnings: List[str]

def evaluate_cache_file_status(data_root: Path, provider_name: str, symbol: str, timeframe: str, start_date: Optional[str], end_date: Optional[str], ttl_seconds: int, force_refresh: bool = False, use_cache: bool = True) -> CacheFileStatus:
    from usa_signal_bot.data.cache import build_market_data_cache_path, cache_exists, is_cache_fresh, cache_file_age_seconds, cache_file_size
    path = build_market_data_cache_path(data_root, provider_name, symbol, timeframe, start_date, end_date)

    exists = cache_exists(path)
    age = cache_file_age_seconds(path)
    size = cache_file_size(path)
    fresh = is_cache_fresh(path, ttl_seconds)

    if not use_cache:
        decision = CacheDecision.BYPASS_CACHE
        reason = "use_cache is False"
    elif force_refresh:
        decision = CacheDecision.REFRESH_CACHE
        reason = "Force refresh enabled"
    elif not exists:
        decision = CacheDecision.CACHE_MISSING
        reason = "Cache file does not exist"
    elif not fresh:
        decision = CacheDecision.CACHE_STALE
        reason = f"Cache is older than TTL ({ttl_seconds}s)"
    else:
        decision = CacheDecision.USE_CACHE
        reason = "Cache is fresh and valid"

    return CacheFileStatus(
        symbol=symbol,
        cache_path=str(path),
        exists=exists,
        is_fresh=fresh,
        age_seconds=age,
        size_bytes=size,
        decision=decision,
        reason=reason
    )

def build_cache_refresh_plan(data_root: Path, request: CacheRefreshRequest, ttl_seconds: int, batch_size: int) -> CacheRefreshPlan:
    from usa_signal_bot.utils.time_utils import utc_now
    import math
    statuses = []
    to_refresh = []
    from_cache = []

    for sym in request.symbols:
        status = evaluate_cache_file_status(
            data_root, request.provider_name, sym, request.timeframe,
            request.start_date, request.end_date, ttl_seconds,
            request.force_refresh, request.use_cache
        )
        statuses.append(status)
        if status.decision in (CacheDecision.REFRESH_CACHE, CacheDecision.CACHE_MISSING, CacheDecision.CACHE_STALE, CacheDecision.CACHE_INVALID, CacheDecision.BYPASS_CACHE):
            to_refresh.append(sym)
        else:
            from_cache.append(sym)

    # Assuming one request per batch
    estimated_reqs = math.ceil(len(to_refresh) / batch_size) if batch_size > 0 else len(to_refresh)

    return CacheRefreshPlan(
        request=request,
        created_at_utc=utc_now().isoformat(),
        statuses=statuses,
        symbols_to_refresh=to_refresh,
        symbols_from_cache=from_cache,
        estimated_requests=estimated_reqs
    )

def cache_refresh_plan_to_text(plan: CacheRefreshPlan) -> str:
    lines = [
        f"Cache Refresh Plan ({plan.request.provider_name} - {plan.request.timeframe})",
        f"Symbols to check: {len(plan.request.symbols)}",
        f"Use Cache: {len(plan.symbols_from_cache)}",
        f"Refresh Required: {len(plan.symbols_to_refresh)}",
        f"Estimated API requests: {plan.estimated_requests}"
    ]
    if plan.symbols_to_refresh:
        lines.append(f"Symbols to refresh: {','.join(plan.symbols_to_refresh[:10])}" + ("..." if len(plan.symbols_to_refresh) > 10 else ""))
    return "\n".join(lines)

def execute_cache_refresh_plan(plan: CacheRefreshPlan, downloader: MarketDataDownloader) -> CacheRefreshResult:
    req = plan.request
    failed = []
    errors = []
    warnings = []
    refreshed = []

    if plan.symbols_to_refresh:
        try:
            resp = downloader.download_for_symbols(
                symbols=plan.symbols_to_refresh,
                timeframe=req.timeframe,
                provider_name=req.provider_name,
                start_date=req.start_date,
                end_date=req.end_date,
                adjusted=True,
                write_cache=True
            )
            if resp.success:
                refreshed = resp.symbols_returned()
            else:
                errors.extend(resp.errors)
            # Find what failed
            for sym in plan.symbols_to_refresh:
                if sym not in refreshed:
                    failed.append(sym)
            warnings.extend(resp.warnings)
        except Exception as e:
            errors.append(f"Refresh execution failed: {e}")
            failed = plan.symbols_to_refresh.copy()

    return CacheRefreshResult(
        plan=plan,
        refreshed_symbols=refreshed,
        cache_used_symbols=plan.symbols_from_cache,
        failed_symbols=failed,
        errors=errors,
        warnings=warnings
    )

def write_cache_refresh_plan_json(path: Path, plan: CacheRefreshPlan) -> Path:
    import json
    from dataclasses import asdict
    from usa_signal_bot.utils.file_utils import safe_mkdir
    safe_mkdir(path.parent)

    d = asdict(plan)
    for s in d['statuses']:
        if hasattr(s['decision'], 'value'):
            s['decision'] = s['decision'].value

    with path.open('w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    return path

def write_cache_refresh_result_json(path: Path, result: CacheRefreshResult) -> Path:
    import json
    from dataclasses import asdict
    from usa_signal_bot.utils.file_utils import safe_mkdir
    safe_mkdir(path.parent)

    d = asdict(result)
    for s in d['plan']['statuses']:
        if hasattr(s['decision'], 'value'):
            s['decision'] = s['decision'].value

    with path.open('w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)
    return path

from .multitimeframe import MultiTimeframeDataRequest
import datetime
import json

from ..core.domain import BaseDomainModel
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class MultiTimeframeRefreshPlan(BaseDomainModel):
    request: MultiTimeframeDataRequest = None
    created_at_utc: str = ""
    plans_by_timeframe: dict[str, CacheRefreshPlan] = field(default_factory=dict)
    total_symbols_to_refresh: int = 0
    total_symbols_from_cache: int = 0
    estimated_requests: int = 0

def build_multitimeframe_refresh_plan(data_root: Path, request: MultiTimeframeDataRequest, ttl_seconds: int, batch_size: int) -> MultiTimeframeRefreshPlan:
    plan = MultiTimeframeRefreshPlan(
        request=request,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    )

    for spec in request.timeframe_specs:
        if not spec.enabled:
            continue

        req = CacheRefreshRequest(
            provider_name=request.provider_name,
            symbols=request.symbols,
            timeframe=spec.timeframe,
            start_date=spec.start_date,
            end_date=spec.end_date,
            force_refresh=request.force_refresh,
            use_cache=request.use_cache
        )
        tf_plan = build_cache_refresh_plan(data_root, req, ttl_seconds, batch_size)
        plan.plans_by_timeframe[spec.timeframe] = tf_plan
        plan.total_symbols_to_refresh += len(tf_plan.symbols_to_refresh)
        plan.total_symbols_from_cache += len(tf_plan.symbols_from_cache)
        plan.estimated_requests += tf_plan.estimated_requests

    return plan

def multitimeframe_refresh_plan_to_text(plan: MultiTimeframeRefreshPlan) -> str:
    lines = [
        f"Multi-Timeframe Refresh Plan ({plan.created_at_utc})",
        f"Provider: {plan.request.provider_name}",
        f"Symbols: {len(plan.request.symbols)}",
        f"Total to refresh: {plan.total_symbols_to_refresh} | Total from cache: {plan.total_symbols_from_cache}",
        f"Estimated requests: {plan.estimated_requests}",
        "---"
    ]
    for tf, tf_plan in plan.plans_by_timeframe.items():
        lines.append(f"Timeframe: {tf}")
        lines.append(f"  To refresh: {len(tf_plan.symbols_to_refresh)}")
        lines.append(f"  From cache: {len(tf_plan.symbols_from_cache)}")
        lines.append(f"  Estimated reqs: {tf_plan.estimated_requests}")
    return "\n".join(lines)

def write_multitimeframe_refresh_plan_json(path: Path, plan: MultiTimeframeRefreshPlan) -> Path:
    from ..core.serialization import dataclass_to_dict
    with open(path, 'w') as f:
        json.dump(dataclass_to_dict(plan), f, indent=2)
    return path
