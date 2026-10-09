import roadtrust


def test_package_imports_from_core() -> None:
    # Fails if the build config stops pointing at core/roadtrust.
    assert roadtrust.__file__ is not None
    assert "core" in roadtrust.__file__
    assert roadtrust.__version__ == "0.0.0"
