import os

from flask import Flask

from . import database as db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(DATABASE=os.path.join(app.instance_path, "link_box.sqlite"))

    _create_instance_dir(app)

    db.init(app)

    @app.cli.command("init-db")
    def create_database():
        db.create()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/")
    def hello():
        return "Hello World"

    return app


def _create_instance_dir(app):
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
