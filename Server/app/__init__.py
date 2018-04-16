from app.config import Config
from flask import Flask

server = Flask(__name__)
server.config.from_object(Config)


import app.controller