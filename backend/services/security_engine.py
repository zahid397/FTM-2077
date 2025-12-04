from backend.config import settings
from datetime import datetime, timedelta

class SecurityEngine:
    def __init__(self):
        self.failed_attempts = 0
        self.blocked_until = None

    def login(self, pwd):
        if self.blocked_until and datetime.now() < self.blocked_until:
            return {"status": "BLOCKED", "message": "Too many attempts."}

        if settings.validate_god_key(pwd):
            self.failed_attempts = 0
            return {"status": "SUCCESS", "mode": "GOD", "message": "God mode access granted."}

        self.failed_attempts += 1
        if self.failed_attempts >= 5:
            self.blocked_until = datetime.now() + timedelta(seconds=30)
            self.failed_attempts = 0
            return {"status": "BLOCKED", "message": "Blocked for 30s."}

        return {"status": "ERROR", "message": "Invalid password"}

security = SecurityEngine()
