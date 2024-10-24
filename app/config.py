from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_host: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    db_port: str = ""
    db_ssl: bool = False


    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        return "postgresql+psycopg2://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
            db_user=self.db_user,
            host=self.db_host,
            password=self.db_password,
            port=self.db_port,
            db_name=self.db_name,
        )

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()