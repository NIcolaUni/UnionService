from .db.calendarioDBmodel import CalendarioDBmodel
from sqlalchemy import desc

class Calendario(CalendarioDBmodel):

    def __init__(self, dipendente, titolo, start_date, end_date, tipologia, luogo=None, descrizione=None, id_evento=None):
        self.dipendente = dipendente
        self.titolo = titolo
        self.start_date = start_date
        self.end_date = end_date
        self.luogo=luogo
        self.tipologia = tipologia #true  evento aziendale, false  evento ferie
        self.descrizione = descrizione
        self.id_evento = id_evento

    def registraEvento(dipendente, titolo, start_date, end_date, tipologia, luogo=None, descrizione=None):

        #se e' un evento e non delle ferie
        if tipologia:

            lastEv=Calendario.query.filter_by(tipologia=True).order_by(desc(Calendario.id_evento)).first()


            if lastEv is None:
                newEvento = Calendario(dipendente=dipendente, titolo=titolo, start_date=start_date,
                                       end_date=end_date, tipologia=tipologia, luogo=luogo,
                                       descrizione=descrizione, id_evento=0)

            else:
                newEvento = Calendario(dipendente=dipendente, titolo=titolo, start_date=start_date,
                                       end_date=end_date, tipologia=tipologia, luogo=luogo,
                                       descrizione=descrizione, id_evento=lastEv.id_evento+1)

        else:
            newEvento = Calendario(dipendente=dipendente, titolo=titolo, start_date=start_date,
                                   end_date=end_date, tipologia=tipologia, luogo=luogo,
                                   descrizione=descrizione)



        CalendarioDBmodel.addRowNoCommit(newEvento)
        CalendarioDBmodel.commit()

    def eliminaEvento(dipendente, titolo, start_date, tipologia):
        toDel = CalendarioDBmodel.query.filter_by(dipendente=dipendente, titolo=titolo, start_date=start_date, tipologia=tipologia).first()

        CalendarioDBmodel.delRow(toDel)

    def modificaFerie(dipendente, newTitolo, oldTitolo, start_date):

        Calendario.query.filter_by(dipendente=dipendente, titolo=oldTitolo, start_date=start_date, tipologia=False).update({'titolo': newTitolo})
        CalendarioDBmodel.commit()