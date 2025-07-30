from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self):
        return (
            "postgresql+psycopg2:"
            f"//{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )


try:
    settings = Settings()  # type: ignore
except Exception:
    raise Exception('Заполните .env или перезапустите терминал')
