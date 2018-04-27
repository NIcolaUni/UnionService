from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

server = Flask(__name__)
server.config.from_object(Config)


database = SQLAlchemy(server)
login_manager = LoginManager(server)
login_manager.login_view = 'login'

socketio = SocketIO(server)

import app.controller

