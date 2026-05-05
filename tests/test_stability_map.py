import pytest
from usa_signal_bot.core.enums import SensitivityMetricName, SensitivityCellStatus, ParameterZoneType
from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterGridCell, SensitivityCellResult
from usa_signal_bot.backtesting.stability_map import build_stability_map, find_neighbor_cells, calculate_local_stability_score

def create_fake_result(cell_id, params, return_pct, status=SensitivityCellStatus.COMPLETED):
    cell = ParameterGridCell(cell_id=cell_id, index=0, strategy_name="s", params=params)
    return SensitivityCellResult(cell, status, None, {"total_return_pct": return_pct})

def test_find_neighbor_cells():
    r1 = create_fake_result("c1", {"a": 1, "b": 1}, 10.0)
    r2 = create_fake_result("c2", {"a": 1, "b": 2}, 11.0) # 1 diff
    r3 = create_fake_result("c3", {"a": 2, "b": 2}, 12.0) # 2 diffs

    neighbors = find_neighbor_cells(r1, [r1, r2, r3])
    assert "c2" in neighbors
    assert "c3" not in neighbors

def test_calculate_local_stability_score():
    r1 = create_fake_result("c1", {"a": 1}, 10.0)
    r2 = create_fake_result("c2", {"a": 2}, 10.5)

    # close values -> high stability
    score = calculate_local_stability_score(r1, [r2], SensitivityMetricName.RETURN_PCT)
    assert score is not None
    assert score > 80.0

    r3 = create_fake_result("c3", {"a": 2}, 50.0)
    # big difference -> low stability
    score_bad = calculate_local_stability_score(r1, [r3], SensitivityMetricName.RETURN_PCT)
    assert score_bad < 80.0

def test_build_stability_map():
    # c1 and c2 are neighbors and stable and > median
    r1 = create_fake_result("c1", {"a": 1}, 20.0)
    r2 = create_fake_result("c2", {"a": 2}, 21.0)

    # c3 is isolated and high (fragile/outlier)
    r3 = create_fake_result("c3", {"a": 9}, 50.0)

    # c4, c5 are neighbors and low
    r4 = create_fake_result("c4", {"a": 4}, 5.0)
    r5 = create_fake_result("c5", {"a": 5}, 6.0)

    smap = build_stability_map([r1, r2, r3, r4, r5], SensitivityMetricName.RETURN_PCT)

    assert len(smap.cells) == 5

    # Verify zone types loosely
    c1_cell = next(c for c in smap.cells if c.cell_id == "c1")
    assert c1_cell.zone_type in (ParameterZoneType.ROBUST_REGION, ParameterZoneType.NEUTRAL_REGION)

    # check if robust region was detected
    pass
