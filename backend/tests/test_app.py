from app.main import create_app


def test_create_app_uses_expected_metadata() -> None:
    app = create_app()

    assert app.title == "HeppySitoUsato API"
    assert app.version == "0.1.0"
