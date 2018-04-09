from flask_login import UserMixin
from app import login_manager

class Dipendente(UserMixin):

    def __init__(self, cf):
        self.CF = cf

@login_manager.user_loader
def load_user(cf):
    return Dipendente.get(cf)
