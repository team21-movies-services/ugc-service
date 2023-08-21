from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    user: str = Field(default='test_perf')
    password: str = Field(default='test_perf')
    database: str = Field(default='test_perf')

    @property
    def postgres_dsn(self) -> dict:
        """Конфиг подключения к postgresql."""
        return {
            'dbname': self.database,
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'port': self.port,
        }
