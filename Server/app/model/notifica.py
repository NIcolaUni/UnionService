from .db.notificaDBmodel import NotificaDBmodel
from sqlalchemy import  func, desc


class Notifica(NotificaDBmodel):

    def __init__(self, destinatario, titolo, contenuto, tipologia, numero, richiedente_ferie=None, start_date=None):
        self.destinatario = destinatario
        self.titolo = titolo
        self.contenuto = contenuto
        self.tipologia = tipologia
        self.numero = numero
        self.richiedente_ferie = richiedente_ferie
        self.start_date = start_date


    # Equivalente al toString() di java
    def __repr__(self):
        return "<Notifica: {0} per il dipendente {1} >".format(self.titolo, self.dipendente)

    '''
        codice veloce per contare. Fonte: https://gist.github.com/hest/8798884
    '''
    def get_counter(destinatario):
        q = NotificaDBmodel.query.filter_by(destinatario=destinatario)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    def registraNotifica( destinatario, titolo, contenuto, tipologia, richiedente_ferie=None, start_date=None):

        notifiche = NotificaDBmodel.query.filter_by(destinatario=destinatario).order_by(desc(NotificaDBmodel.numero)).first()

        if notifiche is None:
            daNotificare = Notifica(destinatario=destinatario, titolo=titolo, contenuto=contenuto, tipologia=tipologia,
                                    numero=1, richiedente_ferie=richiedente_ferie, start_date=start_date)
        else:
            daNotificare = Notifica(destinatario=destinatario, titolo=titolo, contenuto=contenuto, tipologia=tipologia,
                                    numero=notifiche.numero+1, richiedente_ferie=richiedente_ferie, start_date=start_date)

        NotificaDBmodel.addRow(daNotificare)

    def eliminaNotifica(destinatario, numero):
        toDel=NotificaDBmodel.query.filter_by(destinatario=destinatario, numero=numero).first()
        NotificaDBmodel.delRow(toDel)

    def eliminaNotificaFerie(richiedente_ferie, start_date):

        toDel = NotificaDBmodel.query.filter_by(richiedente_ferie=richiedente_ferie, start_date=start_date).all()
        NotificaDBmodel.delRow(toDel)




