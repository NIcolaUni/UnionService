from .db.calendarioDBmodel import CalendarioDBmodel


class Calendario(CalendarioDBmodel):

    def __init__(self, dipendente, titolo, start_date, end_date, luogo, tipologia):
        self.dipendente = dipendente
        self.titolo = titolo
        self.start_date = start_date
        self.end_date = end_date
        self.luogo=luogo
        self.tipologia = tipologia #true  evento aziendale, false  evento ferie

    def registraEvento(dipendente, titolo, start_date, end_date, luogo, tipologia):
        newEvento = Calendario(dipendente=dipendente, titolo=titolo, start_date=start_date,
                               end_date=end_date, tipologia=tipologia, luogo=luogo)
        CalendarioDBmodel.addRow(newEvento)

    def eliminaEvento(dipendente, titolo, start_date, tipologia):
        toDel = CalendarioDBmodel.query.filter_by(dipendente=dipendente, titolo=titolo, start_date=start_date, tipologia=tipologia).first()

        CalendarioDBmodel.delRow(toDel)
