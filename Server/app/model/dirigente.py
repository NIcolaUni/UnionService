from .db.dirigenteDBmodel import DirigenteDBmodel


class Dirigente(DirigenteDBmodel):

    def __init__(self, username):
        self.username = username


    # Equivalente al toString() di java
    def __repr__(self):
        return "<Dirigente - {0} >".format(self.username)
