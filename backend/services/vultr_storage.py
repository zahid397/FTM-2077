import os
from backend.config import settings
import uuid


class VultrStorage:
    def __init__(self):
        self.access = settings.VULTR_ACCESS
        self.secret = settings.VULTR_SECRET
        self.bucket = settings.VULTR_BUCKET
        self.endpoint = settings.VULTR_ENDPOINT.rstrip("/")

        # Fallback URL
        self.local_fallback = "/storage/fallback"

    def is_configured(self) -> bool:
        """Check if real cloud storage is possible."""
        return bool(self.access and self.secret and self.bucket)

    def upload_file(self, filepath: str, remote_name: str = None):
        """
        Safe upload (Hackathon Mode)
        - Never crashes
        - Realistic URL format
        - Works even offline
        """

        if not os.path.exists(filepath):
            print(f"[VULTR ERROR] File not found: {filepath}")
            return None

        # Auto-generate remote name if missing
        if not remote_name:
            rid = uuid.uuid4().hex[:12]
            remote_name = f"reports/{rid}/{os.path.basename(filepath)}"

        # ---------------------------------------------------
        # 1. Fallback (No Credentials)
        # ---------------------------------------------------
        if not self.is_configured():
            print("[VULTR] No credentials. Using safe fallback URL.")
            return f"{self.local_fallback}/{os.path.basename(filepath)}"

        # ---------------------------------------------------
        # 2. Real Cloud Upload (Disabled for Hackathon)
        # ---------------------------------------------------
        try:
            cloud_url = f"{self.endpoint}/{self.bucket}/{remote_name}"

            # Uncomment to use REAL upload:
            # import boto3
            # s3 = boto3.client(
            #     "s3",
            #     endpoint_url=self.endpoint,
            #     aws_access_key_id=self.access,
            #     aws_secret_access_key=self.secret,
            # )
            # s3.upload_file(filepath, self.bucket, remote_name)

            print(f"[VULTR] Simulated Upload → {cloud_url}")
            return cloud_url

        except Exception as e:
            print(f"[VULTR ERROR] {e}")
            return None


# Export instance
vultr = VultrStorage()
