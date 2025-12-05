import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # -----------------------------------------------------
    # BASIC PROJECT DETAILS
    # -----------------------------------------------------
    PROJECT_NAME: str = "FTM-2077 OMEGA"
    VERSION: str = "2.0.77"
    API_PREFIX: str = "/api"

    # -----------------------------------------------------
    # DIRECTORY PATHS
    # -----------------------------------------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    AUDIO_DIR = os.path.join(ROOT_DIR, "backend/audio")
    LOGS_DIR = os.path.join(ROOT_DIR, "backend/logs")
    REPORT_DIR = os.path.join(ROOT_DIR, "backend/reports")
    CACHE_DIR = os.path.join(ROOT_DIR, "backend/cache")

    # -----------------------------------------------------
    # NETWORK SETTINGS (IMPORTANT FOR RAINDROP)
    # -----------------------------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -----------------------------------------------------
    # SECURITY & GOD MODE
    # -----------------------------------------------------
    GOD_MODE: bool = False
    GOD_MODE_KEY: str = os.getenv("GOD_MODE_KEY", "")

    def validate_god_key(self, key):
        return key == self.GOD_MODE_KEY

    # -----------------------------------------------------
    # ELEVENLABS
    # -----------------------------------------------------
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    # -----------------------------------------------------
    # VULTR STORAGE CONFIG
    # -----------------------------------------------------
    VULTR_ACCESS_KEY = os.getenv("VULTR_ACCESS_KEY", "")
    VULTR_SECRET_KEY = os.getenv("VULTR_SECRET_KEY", "")
    VULTR_BUCKET_NAME = os.getenv("VULTR_BUCKET_NAME", "")
    VULTR_ENDPOINT = os.getenv("VULTR_ENDPOINT", "")

    # -----------------------------------------------------
    # LIQUIDMETAL RAINDROP
    # -----------------------------------------------------
    RAINDROP_API_KEY = os.getenv("RAINDROP_API_KEY", "")

    # -----------------------------------------------------
    # AUTO CREATE FOLDERS (NO CRASH)
    # -----------------------------------------------------
    def ensure_folders(self):
        for d in [self.AUDIO_DIR, self.LOGS_DIR, self.REPORT_DIR, self.CACHE_DIR]:
            os.makedirs(d, exist_ok=True)


settings = Settings()
settings.ensure_folders()
