import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.environ.get("PORT", 5000))
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REFRESH_TIMEOUT_SECONDS = int(os.environ.get("REFRESH_TIMEOUT_SECONDS", 30))
