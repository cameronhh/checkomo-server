import config.config as config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api
import os

config = config.config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("CKMO_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("CKMO_SECRET") or "i23jnm2hi0ghn2i0g"
api = Api(app)
db = SQLAlchemy(app)