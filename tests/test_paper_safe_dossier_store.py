import pytest
from pathlib import Path
from usa_signal_bot.paper_safe_dossier.dossier_store import (
    paper_safe_dossiers_dir, non_execution_seals_dir, pre_paper_runtime_maps_dir, paper_safe_dossier_full_reviews_dir,
    paper_safe_dossier_store_dir, paper_safe_dossiers_dir, non_execution_seals_dir, pre_paper_runtime_maps_dir, paper_safe_dossier_full_reviews_dir, write_paper_safe_dossier_json, write_non_execution_seal_json,
    write_pre_paper_runtime_map_json, write_paper_safe_dossier_full_review_json,
    read_paper_safe_dossier_full_review_json, get_latest_paper_safe_dossier_full_review,
    paper_safe_dossier_store_summary
)
from usa_signal_bot.paper_safe_dossier.dossier_report import build_paper_safe_dossier_full_review

def test_paper_safe_dossier_store(tmp_path):
    data_root = tmp_path / "data"

    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}
    review = build_paper_safe_dossier_full_review(payload)

    dossier = review.dossiers[0]
    seal = review.non_execution_seals[0]
    rmap = review.runtime_maps[0]

    # Check creation
    d = paper_safe_dossier_store_dir(data_root)
    assert d.exists()

    # Write components
    write_paper_safe_dossier_json(paper_safe_dossiers_dir(data_root) / f"{dossier.dossier_id}.json", dossier)
    write_non_execution_seal_json(non_execution_seals_dir(data_root) / f"{seal.seal_id}.json", seal)
    write_pre_paper_runtime_map_json(pre_paper_runtime_maps_dir(data_root) / f"{rmap.runtime_map_id}.json", rmap)
    write_paper_safe_dossier_full_review_json(paper_safe_dossier_full_reviews_dir(data_root) / f"{review.review_id}.json", review)

    # Read back
    latest = get_latest_paper_safe_dossier_full_review(data_root)
    assert latest is not None

    read_review = read_paper_safe_dossier_full_review_json(latest)
    assert read_review["review_id"] == review.review_id

    summary = paper_safe_dossier_store_summary(data_root)
    assert summary["dossiers"] == 1
    assert summary["seals"] == 1
    assert summary["runtime_maps"] == 1
    assert summary["full_reviews"] == 1
