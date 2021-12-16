from flask import Flask, jsonify
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError

db = SQLAlchemy()
ma = Marshmallow()
lm = LoginManager()
migrate = Migrate()

def create_app():
    # create the flask app object
    app = Flask(__name__)

    # configure the app
    app.config.from_object("config.app_config")

    db.init_app(app)
    ma.init_app(app)
    lm.init_app(app)
    migrate.init_app(app, db)

    from commands import db_commands
    app.register_blueprint(db_commands)

    # register the routes
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error.messages), 400)

    return app
