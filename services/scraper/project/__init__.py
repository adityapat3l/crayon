from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
toolbar = DebugToolbarExtension()

def create_app(script_info=None):
    app = Flask(__name__)

    # app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object('project.config.BaseConfig')

    # db.init_app(app)
    # toolbar.init_app(app)

    from project.api.bets import bets_blueprint

    app.register_blueprint(bets_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app