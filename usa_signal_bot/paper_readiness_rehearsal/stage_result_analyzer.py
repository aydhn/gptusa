from typing import Any, Dict, List
from collections import Counter
from usa_signal_bot.core.enums import StageRehearsalStatus
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import StageRehearsalResult

def count_stage_statuses(results: List[StageRehearsalResult]) -> Dict[str, int]:
    return dict(Counter(r.status.value for r in results))

def count_stage_safety_flags(results: List[StageRehearsalResult]) -> Dict[str, int]:
    counter = Counter()
    for r in results:
        for flag in r.safety_flags:
            counter[flag.value] += 1
    return dict(counter)

def failed_stage_names(results: List[StageRehearsalResult]) -> List[str]:
    return [r.source_stage for r in results if r.status == StageRehearsalStatus.FAILED]

def blocked_stage_names(results: List[StageRehearsalResult]) -> List[str]:
    return [r.source_stage for r in results if r.status == StageRehearsalStatus.BLOCKED]

def analyze_stage_results(results: List[StageRehearsalResult]) -> Dict[str, Any]:
    return {
        "total_results": len(results),
        "statuses": count_stage_statuses(results),
        "safety_flags": count_stage_safety_flags(results),
        "failed_stages": failed_stage_names(results),
        "blocked_stages": blocked_stage_names(results)
    }

def stage_result_analyzer_to_text(payload: Dict[str, Any]) -> str:
    lines = ["Stage Result Analysis:"]
    lines.append(f"Total Results: {payload.get('total_results', 0)}")
    lines.append(f"Statuses: {payload.get('statuses', {})}")
    lines.append(f"Failed: {payload.get('failed_stages', [])}")
    lines.append(f"Blocked: {payload.get('blocked_stages', [])}")
    return "\n".join(lines)
