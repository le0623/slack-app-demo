import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    def __init__(self):
        self.slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")
        self.slack_app_token: str = os.getenv("SLACK_APP_TOKEN", "")
        self.slack_signing_secret: str = os.getenv("SLACK_SIGNING_SECRET", "")
        self.port: int = int(os.getenv("PORT", "3000"))
        self.host: str = os.getenv("HOST", "0.0.0.0")
        
        if not self.slack_bot_token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required")
        if not self.slack_signing_secret:
            raise ValueError("SLACK_SIGNING_SECRET environment variable is required")


settings = Settings()

