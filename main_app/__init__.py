import os
from datetime import datetime, timedelta

import pymysql
from flask import Flask, g, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

import main_app.config as setting
from main_app.core.middlewares import Middleware

pymysql.install_as_MySQLdb()


import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold

flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func


app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

app.secret_key = 'zxdr%345DFT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{server}/totp'.format(username=setting.DB_USER, password=setting.DB_PASSWORD, server=setting.DB_SERVER)

app.config['JWT_SECRET_KEY'] = 'algofinsjwt'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)


db = SQLAlchemy(app)
marshmallow = Marshmallow(app)
jwt = JWTManager(app)

# app.wsgi_app = Middleware(app.wsgi_app)

from main_app.core.db.models.client_model import ClientData
from main_app.core.db.models.config import Config
from main_app.core.db.models.finger_print import FingerPrintData
from main_app.core.db.models.user import User

db.create_all()

# import templates
from main_app.website.totp_template import totp_route

# register templates
app.register_blueprint(totp_route)

# import apis
from main_app.apis import blueprint as apis_blueprint

app.register_blueprint(apis_blueprint, prefix_url="/api")





