import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "FTM-2077 OMEGA"
    VERSION = "2.0.77"
    API_PREFIX = "/api"

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    GOD_MODE_KEY = os.getenv("GOD_MODE_KEY", "")
    GOD_MODE = bool(GOD_MODE_KEY)

    ROOT_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    BASE_DIR = os.path.join(ROOT_DIR, "backend")

    AUDIO_DIR = os.path.join(BASE_DIR, "audio")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    CACHE_DIR = os.path.join(BASE_DIR, "cache")

    @classmethod
    def init_dirs(cls):
        for path in (
            cls.AUDIO_DIR,
            cls.LOGS_DIR,
            cls.REPORT_DIR,
            cls.CACHE_DIR,
        ):
            os.makedirs(path, exist_ok=True)


Settings.init_dirs()
settings = Settings()
