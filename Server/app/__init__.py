
from app.config import Config
from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
import logging
from app.model.dbManager import DBManager


server = Flask(__name__)
server.config.from_object(Config)

databaseManager = DBManager(server)


login_manager = LoginManager(server)
login_manager.login_view = 'login'

socketio = SocketIO(server)

gunicorn_logger = logging.getLogger('gunicorn.error')
server.logger.handlers = gunicorn_logger.handlers
server.logger.setLevel(gunicorn_logger.level)


import app.controller

