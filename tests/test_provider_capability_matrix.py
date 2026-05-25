
from usa_signal_bot.data_providers.provider_capability_matrix import build_provider_capability_matrix, validate_provider_capability_matrix_safety

def test_provider_capability_matrix():
    matrix = build_provider_capability_matrix()
    assert matrix.matrix_valid is True
    errs = validate_provider_capability_matrix_safety(matrix)
    assert len(errs) == 0
