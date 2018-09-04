from .db.richiestaFerieDBmodel import RichiestaFerieDBmodel
from .calendario import Calendario

class RichiestaFerie(RichiestaFerieDBmodel):

    def __init__(self, dipendente, titolo, start_date, end_date):
        self.dipendente = dipendente
        self.titolo = titolo
        self.start_date = start_date
        self.end_date = end_date



    def registraRichiesta(dipendente, titolo, start_date, end_date):
        newRichiesta = RichiestaFerie(dipendente=dipendente, titolo=titolo, start_date=start_date, end_date=end_date)
        RichiestaFerie.addRow(newRichiesta)

    def eliminaRichiesta(dipendente, start_date):
        toDel = RichiestaFerie.query.filter_by(dipendente=dipendente, start_date=start_date).first()

        RichiestaFerie.delRow(toDel)


    def accettaRichiesta(dipendente, start_date):
        toDel = RichiestaFerie.query.filter_by(dipendente=dipendente, start_date=start_date).first()
        Calendario.registraEvento(dipendente=toDel.dipendente, titolo=toDel.titolo, start_date=toDel.start_date,
                                  end_date=toDel.end_date, tipologia=False, luogo="")
        RichiestaFerie.delRow(toDel)

    def declinaRichiesta(dipendente, start_date):
        RichiestaFerie.eliminaRichiesta(dipendente=dipendente, start_date=start_date)

