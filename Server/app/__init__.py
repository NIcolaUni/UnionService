from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

server = Flask(__name__)
server.config.from_object(Config)


database = SQLAlchemy(server)
login_manager = LoginManager(server)
login_manager.login_view = 'login'

import app.controller

