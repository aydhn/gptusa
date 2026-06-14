"""Tests for the data_provider_runtime module initialization."""

import usa_signal_bot.data_provider_runtime as data_provider_runtime


def test_data_provider_runtime_init_docstring():
    """Verify that the data_provider_runtime module has the expected docstring."""
    assert data_provider_runtime.__doc__ is not None
    assert "Data Provider Runtime module (Phase 107)." in data_provider_runtime.__doc__
    assert (
        "Contains logic for generating cache-aware dry run fetch plans"
        in data_provider_runtime.__doc__
    )
