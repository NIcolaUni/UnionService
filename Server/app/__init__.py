
from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import logging
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



server = Flask(__name__)
server.config.from_object(Config)


database = SQLAlchemy(server)
database.create_all()
migrate = Migrate(server, database)

manager = Manager(server)
manager.add_command('db', MigrateCommand)


login_manager = LoginManager(server)
login_manager.login_view = 'login'

socketio = SocketIO(server)

gunicorn_logger = logging.getLogger('gunicorn.error')
server.logger.handlers = gunicorn_logger.handlers
server.logger.setLevel(gunicorn_logger.level)

accoglienzaForm = None
accoglienzaOk = False
formCercaCliente =None
appUrl="http://192.168.1.131:80"

clienteSelezionato=None
preventivoEdileSelezionato=None
preventivoFinitureSelezionato=None
preventivoVariantiSelezionato=None
rigaPresente = False
tabellaRigaPresente = None
prezzarioProdottiTipoCorrente = None

import app.controller

