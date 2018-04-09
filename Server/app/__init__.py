from app.config import Config
from flask import Flask
from flask_login import LoginManager

server = Flask(__name__)
server.config.from_object(Config)

login_manager = LoginManager(server)

import app.controller