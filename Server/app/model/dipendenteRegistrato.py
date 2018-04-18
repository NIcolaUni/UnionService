from flask_login import UserMixin
from app import login_manager
from app.model.db.dipRegistratoDBmodel import DipRegistratoDBmodel

class DipendenteRegistrato(UserMixin, DipRegistratoDBmodel):

    def __init__(self, username, password, fittizio):
        self.username = username
        self.password = password
        self.fittizio = fittizio

    def __repr__(self):
        return "DipendenteRegistrato {0}".format(self.username)

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return DipendenteRegistrato.query.get(username)
