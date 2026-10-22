from dishka import Scope
from orderflow_core.database.sqlalchemy import DatabaseConfig
from orderflow_core.di import injectable
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_HOST: str = Field(...)
    POSTGRES_PORT: int = Field(...)
    POSTGRES_DB: str = Field(...)

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    APP_HOST_PORT: int = Field(...)

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@injectable(scope=Scope.APP)
def config() -> Config:
    return Config()


@injectable(scope=Scope.APP)
def database_config(config: Config) -> DatabaseConfig:
    return DatabaseConfig(
        url=config.database_url,
    )
