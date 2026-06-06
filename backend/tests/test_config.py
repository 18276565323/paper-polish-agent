from app.core.config import Settings


def test_settings_use_safe_modelgate_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_env == "local"
    assert settings.modelgate_base_url == "https://mg.aid.pub/v1"
    assert settings.modelgate_api_key == ""
    assert settings.modelgate_model == ""
    assert settings.database_url == "sqlite:///./paper_polish_dev.db"
