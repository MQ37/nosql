import os

from flask import Flask, render_template

from webapp.flaskr.db import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(SECRET_KEY='dev')

    # config and test config
    if test_config is None:
        app.config.from_pyfile('config.py', silent=False)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # register blueprints
    from . import orders, drivers
    app.register_blueprint(orders.bp)
    app.register_blueprint(drivers.bp)

    # index view
    @app.route('/')
    def index_view():
        return render_template("index.html")

    return app
