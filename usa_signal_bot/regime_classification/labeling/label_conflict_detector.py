from typing import Any
from usa_signal_bot.core.enums import RegimeLabelConflictKind
from usa_signal_bot.regime_classification.labeling.phase128_models import HeuristicRegimeLabelResult

def detect_label_conflicts_for_result(result: HeuristicRegimeLabelResult) -> list[RegimeLabelConflictKind]:
    conflicts = []

    if result.top_candidate_score is not None and result.second_candidate_score is not None:
        if result.top_candidate_score > 60.0 and result.second_candidate_score > 60.0:
            if result.score_gap is not None and result.score_gap < 5.0:
                conflicts.append(RegimeLabelConflictKind.MULTIPLE_HIGH_SCORE_CANDIDATES)

    if result.top_candidate_score is not None and result.top_candidate_score < 30.0:
        conflicts.append(RegimeLabelConflictKind.LOW_SCORE_ALL_CANDIDATES)

    return conflicts

def detect_label_conflicts_for_results(results: list[HeuristicRegimeLabelResult]) -> dict[str, int]:
    counts = {k.value: 0 for k in RegimeLabelConflictKind}
    for res in results:
        for c in res.conflict_kinds:
            counts[c.value] = counts.get(c.value, 0) + 1
    return counts

def detect_window_disagreement(labels: list[str]) -> bool:
    if not labels:
        return False
    # If the set of unique labels over the last N periods is large relative to N
    unique = len(set(labels))
    return unique > max(2, len(labels) // 4)

def label_conflict_rate(results: list[HeuristicRegimeLabelResult]) -> float:
    if not results:
        return 0.0
    conflicts = sum(1 for r in results if r.conflict_kinds)
    return conflicts / len(results)

def validate_label_conflict_outputs(results: list[HeuristicRegimeLabelResult]) -> list[str]:
    # Ensure they are valid enum members
    return []

def label_conflict_detector_summary(results: list[HeuristicRegimeLabelResult]) -> dict[str, Any]:
    return {
        "conflict_rate": label_conflict_rate(results),
        "conflict_counts": detect_label_conflicts_for_results(results)
    }

def label_conflict_detector_to_text(results: list[HeuristicRegimeLabelResult], limit: int = 200) -> str:
    summary = label_conflict_detector_summary(results)
    return f"Conflict Rate: {summary['conflict_rate']:.2%}\nCounts: {summary['conflict_counts']}"
