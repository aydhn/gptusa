import datetime
from typing import Dict, Any, List
import pandas as pd
from .phase147_models import (
    ResearchDecisionRecord,
    ResearchDecisionStream,
    BacktestRunConfig,
    ResearchDecisionKind,
    ResearchExposureSide,
    create_research_decision_record_id,
    create_research_decision_stream_id,
)


def infer_research_decision_record(
    row: Dict[str, Any], config: BacktestRunConfig
) -> ResearchDecisionRecord:
    score = row.get("research_prediction_score", 0.0)
    kind = ResearchDecisionKind.NO_ACTION_METADATA
    side = ResearchExposureSide.FLAT
    if score > 0.5:
        kind = ResearchDecisionKind.ENTER_EXPOSURE_METADATA
        side = config.exposure_side

    return ResearchDecisionRecord(
        decision_id=create_research_decision_record_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        symbol=row["symbol"],
        timestamp=row["timestamp"],
        decision_kind=kind,
        exposure_side=side,
        research_score=score,
        research_label=row.get("research_prediction_label"),
        source_prediction_id=row.get("source_prediction_id"),
        deterministic_rank=None,
        not_live_signal=True,
        not_order_decision=True,
        not_investment_advice=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={},
    )


def build_research_decision_stream(
    prediction_df: pd.DataFrame, config: BacktestRunConfig
) -> ResearchDecisionStream:
    records = [
        infer_research_decision_record(row, config)
        for row in prediction_df.to_dict("records")
    ]

    symbols = list(prediction_df["symbol"].unique()) if not prediction_df.empty else []
    timestamps = (
        sorted(prediction_df["timestamp"].unique()) if not prediction_df.empty else []
    )
    start = timestamps[0] if timestamps else None
    end = timestamps[-1] if timestamps else None

    return ResearchDecisionStream(
        stream_id=create_research_decision_stream_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        records=records,
        row_count=len(records),
        symbols=symbols,
        start_timestamp=start,
        end_timestamp=end,
        stream_hash=None,
        stream_valid=True,
        deterministic=True,
        research_data_only=True,
        offline_backtest_research_only=True,
        produces_live_signal=False,
        produces_order_decision=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={},
    )


def validate_research_decision_stream(stream: ResearchDecisionStream) -> List[str]:
    errors = []
    if stream.produces_live_signal:
        errors.append("Stream produces live signal")
    if stream.produces_order_decision:
        errors.append("Stream produces order decision")
    if stream.investment_advice:
        errors.append("Stream is marked as investment advice")
    return errors


def compute_research_decision_stream_hash(stream: ResearchDecisionStream) -> str:
    import hashlib

    data = "".join(
        [f"{r.symbol}{r.timestamp}{r.decision_kind.value}" for r in stream.records]
    )
    return hashlib.sha256(data.encode()).hexdigest()


def research_decision_stream_to_dataframe(
    stream: ResearchDecisionStream,
) -> pd.DataFrame:
    return pd.DataFrame([r.__dict__ for r in stream.records])


def research_decision_stream_summary(stream: ResearchDecisionStream) -> Dict[str, Any]:
    return {"row_count": stream.row_count, "symbols": stream.symbols}


def research_decision_stream_to_text(
    stream: ResearchDecisionStream, limit: int = 300
) -> str:
    return f"ResearchDecisionStream {stream.stream_id} with {stream.row_count} records"
