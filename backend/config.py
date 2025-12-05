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
    # DIRECTORY PATHS (FIXED)
    # -----------------------------------------------------
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    BASE_DIR = os.path.join(ROOT_DIR, "backend")

    AUDIO_DIR = os.path.join(BASE_DIR, "audio")
    LOGS_DIR = os.path.join(BASE_DIR, "logs")
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    CACHE_DIR = os.path.join(BASE_DIR, "cache")

    # -----------------------------------------------------
    # NETWORK SETTINGS
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
    ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    # -----------------------------------------------------
    # VULTR STORAGE CONFIG  (NAME FIXED)
    # -----------------------------------------------------
    VULTR_ACCESS = os.getenv("VULTR_ACCESS_KEY", "")
    VULTR_SECRET = os.getenv("VULTR_SECRET_KEY", "")
    VULTR_BUCKET = os.getenv("VULTR_BUCKET_NAME", "")
    VULTR_ENDPOINT = os.getenv("VULTR_ENDPOINT", "https://ewr1.vultrobjects.com")

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
