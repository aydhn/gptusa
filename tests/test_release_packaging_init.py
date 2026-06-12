import usa_signal_bot.release_packaging as release_packaging


def test_release_packaging_module_docstring():
    """Verify that the release_packaging module has the expected docstring."""
    assert release_packaging.__doc__ is not None
    assert (
        "USA Signal Bot - Safe Local Release Packaging Module"
        in release_packaging.__doc__
    )
