import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "FTM-2077 OMEGA"
    VERSION: str = "2.0.77"
    API_PREFIX: str = "/api"

    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")

    GOD_MODE_KEY: str = Field("", env="GOD_MODE_KEY")
    GOD_MODE: bool = False

    ROOT_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    BASE_DIR: str = os.path.join(ROOT_DIR, "backend")

    AUDIO_DIR: str = os.path.join(BASE_DIR, "audio")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")
    REPORT_DIR: str = os.path.join(BASE_DIR, "reports")
    CACHE_DIR: str = os.path.join(BASE_DIR, "cache")

    class Config:
        env_file = ".env"

    def __init__(self, **values):
        super().__init__(**values)
        self.GOD_MODE = bool(self.GOD_MODE_KEY)
        for path in (
            self.AUDIO_DIR,
            self.LOGS_DIR,
            self.REPORT_DIR,
            self.CACHE_DIR,
        ):
            os.makedirs(path, exist_ok=True)


settings = Settings()
