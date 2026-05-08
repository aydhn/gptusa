from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid

from usa_signal_bot.core.enums import ComparisonMetricStatus, SignalDriftStatus
from usa_signal_bot.comparison.comparison_models import SignalDriftMetrics, SignalDriftPair, SignalSnapshot

def signal_snapshot_from_signal_record(record: Dict[str, Any], source: Optional[str] = None) -> SignalSnapshot:
    return SignalSnapshot(
        snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
        signal_id=record.get("signal_id", record.get("id")),
        candidate_id=None,
        symbol=record.get("symbol", "unknown"),
        timeframe=record.get("timeframe", "1d"),
        strategy_name=record.get("strategy_name"),
        action=record.get("action", record.get("direction")),
        score=record.get("score"),
        confidence=record.get("confidence"),
        rank_score=None,
        feature_snapshot=record.get("features", {}),
        created_at_utc=record.get("created_at_utc", record.get("timestamp")),
        source=source
    )

def signal_snapshot_from_candidate_record(record: Dict[str, Any], source: Optional[str] = None) -> SignalSnapshot:
    return SignalSnapshot(
        snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
        signal_id=record.get("signal_id"),
        candidate_id=record.get("candidate_id", record.get("id")),
        symbol=record.get("symbol", "unknown"),
        timeframe=record.get("timeframe", "1d"),
        strategy_name=record.get("strategy_name"),
        action=record.get("action", record.get("direction")),
        score=record.get("score"),
        confidence=record.get("confidence"),
        rank_score=record.get("rank_score", record.get("rank")),
        feature_snapshot=record.get("features", {}),
        created_at_utc=record.get("created_at_utc", record.get("timestamp")),
        source=source
    )

def compare_signal_snapshots(original: SignalSnapshot, replay: SignalSnapshot) -> SignalDriftPair:
    score_gap = abs(original.score - replay.score) if original.score is not None and replay.score is not None else None
    conf_gap = abs(original.confidence - replay.confidence) if original.confidence is not None and replay.confidence is not None else None
    rank_gap = abs(original.rank_score - replay.rank_score) if original.rank_score is not None and replay.rank_score is not None else None

    feat_gap = calculate_feature_gap_score(original.feature_snapshot, replay.feature_snapshot)

    changed_action = False
    if original.action and replay.action and original.action.lower() != replay.action.lower():
        changed_action = True

    status = classify_signal_drift_status(score_gap, conf_gap, rank_gap, feat_gap, changed_action)

    return SignalDriftPair(
        pair_id=f"drift_{uuid.uuid4().hex[:8]}",
        symbol=original.symbol,
        timeframe=original.timeframe,
        original_snapshot_id=original.snapshot_id,
        replay_snapshot_id=replay.snapshot_id,
        drift_status=status,
        score_gap=score_gap,
        confidence_gap=conf_gap,
        rank_gap=rank_gap,
        feature_gap_score=feat_gap,
        changed_action=changed_action,
        warnings=[],
        errors=[]
    )

def calculate_feature_gap_score(original_features: Dict[str, Any], replay_features: Dict[str, Any]) -> Optional[float]:
    if not original_features or not replay_features:
        return None

    gaps = []
    for k, v1 in original_features.items():
        v2 = replay_features.get(k)
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            if v1 != 0:
                gaps.append(abs((v1 - v2) / v1))
            elif v2 != 0:
                gaps.append(1.0)
            else:
                gaps.append(0.0)

    if not gaps:
        return None
    return sum(gaps) / len(gaps)

def calculate_signal_drift_metrics(pairs: List[SignalDriftPair]) -> SignalDriftMetrics:
    if not pairs:
        return SignalDriftMetrics(
            status=ComparisonMetricStatus.EMPTY,
            compared_signal_count=0,
            missing_signal_count=0,
            changed_signal_count=0,
            changed_candidate_count=0,
            score_drift_average=None,
            confidence_drift_average=None,
            rank_drift_average=None,
            feature_drift_average=None,
            drift_status=SignalDriftStatus.INSUFFICIENT_DATA,
            warnings=[],
            errors=[]
        )

    scores = [p.score_gap for p in pairs if p.score_gap is not None]
    confs = [p.confidence_gap for p in pairs if p.confidence_gap is not None]
    ranks = [p.rank_gap for p in pairs if p.rank_gap is not None]
    feats = [p.feature_gap_score for p in pairs if p.feature_gap_score is not None]

    changed = sum(1 for p in pairs if p.changed_action)

    avg_score = sum(scores) / len(scores) if scores else None
    avg_conf = sum(confs) / len(confs) if confs else None
    avg_rank = sum(ranks) / len(ranks) if ranks else None
    avg_feat = sum(feats) / len(feats) if feats else None

    overall_status = classify_signal_drift_status(avg_score, avg_conf, avg_rank, avg_feat, changed > 0)

    return SignalDriftMetrics(
        status=ComparisonMetricStatus.OK,
        compared_signal_count=len(pairs),
        missing_signal_count=0, # Computed separately
        changed_signal_count=changed,
        changed_candidate_count=0,
        score_drift_average=avg_score,
        confidence_drift_average=avg_conf,
        rank_drift_average=avg_rank,
        feature_drift_average=avg_feat,
        drift_status=overall_status,
        warnings=[],
        errors=[]
    )

def classify_signal_drift_status(score_gap: Optional[float], confidence_gap: Optional[float], rank_gap: Optional[float], feature_gap_score: Optional[float], changed_action: bool) -> SignalDriftStatus:
    if changed_action:
        return SignalDriftStatus.SEVERE_DRIFT

    max_drift = 0.0
    if feature_gap_score is not None:
        max_drift = max(max_drift, feature_gap_score)
    if confidence_gap is not None:
        max_drift = max(max_drift, confidence_gap)

    if max_drift > 0.5:
        return SignalDriftStatus.HIGH_DRIFT
    if max_drift > 0.2:
        return SignalDriftStatus.MODERATE_DRIFT
    if max_drift > 0.05:
        return SignalDriftStatus.LOW_DRIFT

    return SignalDriftStatus.NO_DRIFT

def match_signal_snapshots(originals: List[SignalSnapshot], replays: List[SignalSnapshot]) -> List[SignalDriftPair]:
    pairs = []
    replay_dict = {}
    for r in replays:
        key = r.signal_id or r.candidate_id or f"{r.symbol}_{r.timeframe}_{r.strategy_name}_{r.created_at_utc}"
        replay_dict[key] = r

    for o in originals:
        key = o.signal_id or o.candidate_id or f"{o.symbol}_{o.timeframe}_{o.strategy_name}_{o.created_at_utc}"
        r = replay_dict.get(key)
        if r:
            pairs.append(compare_signal_snapshots(o, r))

    return pairs

def signal_snapshot_to_dict(snapshot: SignalSnapshot) -> dict:
    from dataclasses import asdict
    return asdict(snapshot)

def signal_drift_pair_to_dict(pair: SignalDriftPair) -> dict:
    from dataclasses import asdict
    d = asdict(pair)
    if isinstance(d.get("drift_status"), SignalDriftStatus):
        d["drift_status"] = d["drift_status"].value
    return d

def signal_drift_metrics_to_text(metrics: SignalDriftMetrics) -> str:
    lines = ["Signal Drift Metrics:"]
    lines.append(f"  Compared: {metrics.compared_signal_count}")
    lines.append(f"  Changed Actions: {metrics.changed_signal_count}")
    lines.append(f"  Status: {metrics.drift_status.value}")
    return "\n".join(lines)
