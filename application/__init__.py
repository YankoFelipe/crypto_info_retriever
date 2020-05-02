from flask_cors import CORS
from flask import Flask
from application.config import Config as AppConfig
from flask_migrate import Migrate
from data.repositories.postgres.entities import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(AppConfig.get())

    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    cors = CORS(app, resources={r"*": {"origins": "*"}})
    return app
