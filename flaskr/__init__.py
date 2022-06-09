import imp
import os
import requests
from flask import ( Flask, render_template)
from datetime import (date, timedelta)

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
       SECRET_KEY='dev',
       DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
       )
    if test_config is None:
           # load the instance config, if it exists, when not testing
       app.config.from_pyfile('config.py', silent=True)
    else :
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import charts
    app.register_blueprint(charts.bp)

    from . import pred
    app.register_blueprint(pred.bp)
    return app
