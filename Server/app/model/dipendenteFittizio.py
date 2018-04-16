from flask_login import UserMixin
from app import LoginManager
from app.model.db.dipFittizioDBmodel import DipFittizioDBmodel

class DipendenteFittizio(UserMixin, DipFittizioDBmodel):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "DipendenteFittizio - {0}".format(self.username)


@login_manager.user_loader
def load_user(username):
    return DipendenteFittizio.query.get(username)