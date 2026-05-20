from usa_signal_bot.paper_observation.observation_models import ObservationReview

def observation_limitations_text() -> str:
    return "LIMITATIONS: No broker order, no live/demo order, no active paper enable, no paper mutation, no Telegram real send. This is NOT investment advice."

def observation_review_to_text(review: ObservationReview, limit: int = 100) -> str:
    lines = [f"Observation Review {review.review_id}", observation_limitations_text()]
    return "\n".join(lines)
