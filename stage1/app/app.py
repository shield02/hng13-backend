import os

from flask import Flask
from .string_analyzer import string_bp

app = Flask(__name__)
app.register_blueprint(string_bp)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000))
    )
