import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getcwd())

class Settings:
    PROJECT_NAME = "FTM-2077 OMEGA"
    VERSION = "3.0.0"
    API_PREFIX = "/api"

    try:
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    except NameError:
        BASE_DIR = os.getcwd()

    BACKEND_DIR = os.path.join(BASE_DIR, "backend")
    STORAGE_DIR = os.path.join(BACKEND_DIR, "storage")
    REPORT_DIR = os.path.join(STORAGE_DIR, "reports")
    AUDIO_DIR = os.path.join(STORAGE_DIR, "audio")

    HOST = "0.0.0.0"
    PORT = 8000
    GOD_MODE = False
    GOD_KEY = os.getenv("GOD_MODE_KEY", "OMEGA-777")

    CEREBRAS_KEY = os.getenv("CEREBRAS_API_KEY")
    ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    VULTR_ACCESS = os.getenv("VULTR_ACCESS_KEY")
    VULTR_SECRET = os.getenv("VULTR_SECRET_KEY")
    VULTR_BUCKET = os.getenv("VULTR_BUCKET_NAME")
    VULTR_ENDPOINT = os.getenv("VULTR_ENDPOINT")

    def validate_god_key(self, key: str):
        if not key: return False
        return key.strip() == self.GOD_KEY

settings = Settings()

os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
