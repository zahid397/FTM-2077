from backend.config import settings
from datetime import datetime, timedelta
import hashlib


class SecurityEngine:
    def __init__(self):
        self.failed_attempts = {}
        self.blocked_until = {}

    # -------------------------
    # Hash Function (SHA256)
    # -------------------------
    def hash(self, text: str):
        return hashlib.sha256(text.encode()).hexdigest()

    # -------------------------
    # Validate Key
    # -------------------------
    def validate_god_key(self, input_key):
        if not settings.GOD_KEY:
            return False
        return self.hash(input_key) == self.hash(settings.GOD_KEY)

    # -------------------------
    # Login Handler
    # -------------------------
    def login(self, pwd: str, ip: str = "LOCAL"):
        now = datetime.now()

        # BLOCK CHECK
        if ip in self.blocked_until and now < self.blocked_until[ip]:
            remaining = int((self.blocked_until[ip] - now).total_seconds())
            return {
                "status": "BLOCKED",
                "message": f"Too many attempts. Try again in {remaining}s."
            }

        # SUCCESS CASE
        if self.validate_god_key(pwd):
            self.failed_attempts[ip] = 0
            return {
                "status": "SUCCESS",
                "mode": "GOD",
                "message": "GOD MODE ACTIVATED."
            }

        # FAILURE CASE
        self.failed_attempts[ip] = self.failed_attempts.get(ip, 0) + 1

        if self.failed_attempts[ip] >= 5:
            self.blocked_until[ip] = now + timedelta(seconds=30)
            self.failed_attempts[ip] = 0
            return {
                "status": "BLOCKED",
                "message": "Locked for 30 seconds."
            }

        return {
            "status": "ERROR",
            "message": "Invalid password."
        }


security = SecurityEngine()
