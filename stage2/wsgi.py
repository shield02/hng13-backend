from src.app import create_app
from src.config import Config

config = Config()

app = create_app(config)
