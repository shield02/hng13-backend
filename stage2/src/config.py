import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration settings for the Flask application.
    """
    PORT = int(os.environ.get("PORT", 5000))

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "mysql+pymysql://hng13:stage2@db:3306/country_currency_exchange")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REFRESH_TIMEOUT_SECONDS = int(os.environ.get("REFRESH_TIMEOUT_SECONDS", 30))
