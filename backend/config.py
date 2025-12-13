import os
from dotenv import load_dotenv

# 🔒 HARDENED IMPORT (pydantic v1 + v2 safe)
try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    from pydantic import BaseSettings, Field

load_dotenv()


class Settings(BaseSettings):
    # -----------------------------------------------------
    # BASIC PROJECT DETAILS
    # -----------------------------------------------------
    PROJECT_NAME: str = "FTM-2077 OMEGA"
    VERSION: str = "2.0.77"
    API_PREFIX: str = "/api"

    # -----------------------------------------------------
    # NETWORK SETTINGS
    # -----------------------------------------------------
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # -----------------------------------------------------
    # SECURITY & GOD MODE
    # -----------------------------------------------------
    GOD_MODE_KEY: str = Field(default="", env="GOD_MODE_KEY")
    GOD_MODE: bool = False

    # -----------------------------------------------------
    # DIRECTORY PATHS
    # -----------------------------------------------------
    ROOT_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    BASE_DIR: str = os.path.join(ROOT_DIR, "backend")

    AUDIO_DIR: str = os.path.join(BASE_DIR, "audio")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")
    REPORT_DIR: str = os.path.join(BASE_DIR, "reports")
    CACHE_DIR: str = os.path.join(BASE_DIR, "cache")

    # -----------------------------------------------------
    # POST INIT
    # -----------------------------------------------------
    def __init__(self, **values):
        super().__init__(**values)

        # Auto-enable GOD MODE
        self.GOD_MODE = bool(self.GOD_MODE_KEY)

        # Ensure directories exist
        for path in (
            self.AUDIO_DIR,
            self.LOGS_DIR,
            self.REPORT_DIR,
            self.CACHE_DIR,
        ):
            os.makedirs(path, exist_ok=True)


# 🔥 SINGLETON INSTANCE
settings = Settings()
