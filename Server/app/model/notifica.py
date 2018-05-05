from app.model.db.notificaDBmodel import NotificaDBmodel
from sqlalchemy import  func


class Notifica(NotificaDBmodel):

    def __init__(self, dipendente, titolo, contenuto):
        self.dipendente = dipendente
        self.titolo = titolo
        self.contenuto = contenuto


    # Equivalente al toString() di java
    def __repr__(self):
        return "<Notifica: {0} per il dipendente {1} >".format(self.titolo, self.dipendente)

    '''
        codice veloce per contare. Fonte: https://gist.github.com/hest/8798884
    '''
    def get_counter(dipendente):
        q = NotificaDBmodel.query.filter_by(dipendente=dipendente)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count
