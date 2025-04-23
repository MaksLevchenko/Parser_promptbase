from pathlib import Path

from pydantic import model_validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Конфигурация модели
    model_config = SettingsConfigDict(
        env_file="../local.env",  # Файл с переменными окружения
        extra="ignore",  # Игнорируем лишние значения в env файле
    )

    # app = FastAPI() params
    app_root_path: str = ""
    app_openapi_url: str = ""
    app_swagger_url: str | None = "/docs"
    app_version: str = "0.0.1"


    @model_validator(mode="after")
    def setting_validator(self) -> "Settings":
        file_version = ".version"
        if Path(file_version).exists():
            with open(file_version, "r") as fp:
                self.app_version = fp.readline()


        return self


settings = Settings()
