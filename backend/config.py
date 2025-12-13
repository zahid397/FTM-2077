import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # BASIC PROJECT DETAILS
    PROJECT_NAME: str = "FTM-2077 OMEGA"
    VERSION: str = "2.0.77"
    API_PREFIX: str = "/api"

    # NETWORK
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # SECURITY
    GOD_MODE_KEY: str = Field(default="")
    GOD_MODE: bool = False

    # PATHS
    ROOT_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    BASE_DIR: str = os.path.join(ROOT_DIR, "backend")

    AUDIO_DIR: str = os.path.join(BASE_DIR, "audio")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")
    REPORT_DIR: str = os.path.join(BASE_DIR, "reports")
    CACHE_DIR: str = os.path.join(BASE_DIR, "cache")

    # 🔥 Pydantic v2 config
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

    def model_post_init(self, __context):
        self.GOD_MODE = bool(self.GOD_MODE_KEY)
        for path in (
            self.AUDIO_DIR,
            self.LOGS_DIR,
            self.REPORT_DIR,
            self.CACHE_DIR,
        ):
            os.makedirs(path, exist_ok=True)


settings = Settings()
