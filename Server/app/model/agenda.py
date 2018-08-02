from .db.agendaDBmodel import AgendaDBmodel

class Agenda(AgendaDBmodel):

    def __init__(self, dipendente, titolo, start_date, durata_giorni, tipologia, start_hour=None,
                  durata_ore=None, accompagnatore_sopraluogo=None, cliente_sopraluogo=None, sopraluogo=False,
                 luogo_sopraluogo=None):

        self.dipendente = dipendente
        self.titolo = titolo
        self.start_date = start_date
        self.durata_giorni = durata_giorni
        self.tipologia = tipologia

        self.start_hour=start_hour
        self.durata_ore=durata_ore
        self.accompagnatore_sopraluogo=accompagnatore_sopraluogo
        self.cliente_sopraluogo=cliente_sopraluogo
        self.sopraluogo = sopraluogo
        self.luogo_sopraluogo=luogo_sopraluogo


    def registraEvento( dipendente, titolo, start_date, durata_giorni, tipologia, start_hour=None,
                  durata_ore=None, accompagnatore_sopraluogo=None, cliente_sopraluogo=None, sopraluogo=False,
                    luogo_sopraluogo=None):

        newEvento = Agenda(dipendente=dipendente, titolo=titolo, start_date=start_date,
                           durata_giorni=durata_giorni, tipologia=tipologia, start_hour=start_hour,
                           durata_ore=durata_ore, accompagnatore_sopraluogo=accompagnatore_sopraluogo, cliente_sopraluogo=cliente_sopraluogo,
                           sopraluogo=sopraluogo, luogo_sopraluogo=luogo_sopraluogo)
        AgendaDBmodel.addRow(newEvento)

    def eliminaEvento( dipendente, titolo, start_date ):

        toDel = AgendaDBmodel.query.filter_by(dipendente=dipendente, titolo=titolo, start_date=start_date).first()

        AgendaDBmodel.delRow(toDel)
