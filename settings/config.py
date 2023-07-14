import os
from pathlib import Path

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    redis_url: SecretStr
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
config = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = os.path.join(BASE_DIR, 'locales')
DOMAIN = 'BOT_SWIPE'