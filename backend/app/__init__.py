import os
from flask import Flask
from .routes import main
from .tasks import executor

def create_app():
    app = Flask(__name__)

    os.makedirs("app/uploads", exist_ok=True)
    os.makedirs("app/static/results", exist_ok=True)

    app.register_blueprint(main)

    return app