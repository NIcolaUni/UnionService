from flask_login import UserMixin
from app import login_manager
from app.model.db.dipFittizioDBmodel import DipFittizioDBmodel

class DipendenteFittizio(UserMixin, DipFittizioDBmodel):

    def __init__(self, username, password, classe, dirigente):
        self.username = username
        self.password = password
        self.classe = classe
        self.dirigente = dirigente

    def __repr__(self):
        return "DipendenteFittizio - {0}".format(self.username)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return DipendenteFittizio.query.get(username)
