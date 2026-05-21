from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PromotionDossierReportType
from .dossier_models import (
    PromotionDossierReview,
    create_promotion_dossier_review_id,
    ObserverPromotionDossier,
    FinalSafetyBoardReview,
    StagedPaperReadinessPackage
)

def build_promotion_dossier_review(
    dossier: ObserverPromotionDossier,
    board_review: Optional[FinalSafetyBoardReview] = None,
    package: Optional[StagedPaperReadinessPackage] = None
) -> PromotionDossierReview:
    return PromotionDossierReview(
        review_id=create_promotion_dossier_review_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        report_type=PromotionDossierReportType.FULL_PROMOTION_DOSSIER_REVIEW,
        dossiers=[dossier],
        board_reviews=[board_review] if board_review else [],
        readiness_packages=[package] if package else [],
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def promotion_dossier_review_summary(review: PromotionDossierReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "dossiers": len(review.dossiers),
        "board_reviews": len(review.board_reviews),
        "readiness_packages": len(review.readiness_packages)
    }

def promotion_dossier_limitations_text() -> str:
    return (
        "LIMITATIONS: No broker order. No live order. No demo order. "
        "No active paper enable. No real paper state mutation. "
        "No Telegram real send. No production config patch. "
        "Safety board decision is NOT a deployment approval. "
        "Readiness package is NOT an activation. "
        "NOT investment advice."
    )

def promotion_dossier_review_to_text(review: PromotionDossierReview, limit: int = 100) -> str:
    lines = [
        f"Promotion Dossier Review: {review.review_id}",
        promotion_dossier_limitations_text(),
        f"Dossiers: {len(review.dossiers)}",
        f"Board Reviews: {len(review.board_reviews)}",
        f"Packages: {len(review.readiness_packages)}"
    ]
    return "\n".join(lines)
