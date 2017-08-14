import os
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

def create_app(config_filepath = "resource/config.cfg"):

    from codeMarble_config import *
    app.config.from_object(codeMarbleConfig)
    app.config.from_pyfile(config_filepath, silent=True)

    from codeMarble_py3des import TripleDES
    TripleDES.init()

    from codeMarble_logger import Log
    Log.init()

    from cache_session import SimpleCacheSessionInterface
    app.session_interface = SimpleCacheSessionInterface()

    from database import DBManager
    DBManager.init(app.config['DB_URL'])
    DBManager.init_db()

    from controller import *
    from codeMarble_blueprint import codeMarble
    app.register_blueprint(codeMarble)

    return app

# @app.error_handler(404)
# @app.error_handler(500)
# def page_not_found(e = None):
#     return render_template("404.html")
