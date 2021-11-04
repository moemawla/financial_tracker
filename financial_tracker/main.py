from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    # configuring our app:
    app.config.from_object("config.app_config")

    db.init_app(app)
    ma.init_app(app)

    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app
