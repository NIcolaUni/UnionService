from .db.assistenzaLavorazioneDBmodel import AssistenzaLavorazioneDBmodel

class AssistenzaLavorazione(AssistenzaLavorazioneDBmodel):

    def __init__(self, nome, costo, prezzoPercentuale, tipologia_lavorazione, settore):

        self.nome = nome
        self.costo = costo
        self.prezzoPercentuale = prezzoPercentuale
        self.tipologia_lavorazione = tipologia_lavorazione
        self.settore = settore


    def registraAssistenza(nome, costo, prezzoPercentuale, tipologia_lavorazione, settore):

        #In caso esistesse già non faccio nulla
        old = AssistenzaLavorazione.query.filter_by(nome=nome, tipologia_lavorazione=tipologia_lavorazione,
                                                    settore=settore).first()

        if old is None:
            new = AssistenzaLavorazione(nome=nome, costo=costo, prezzoPercentuale=prezzoPercentuale,
                                        tipologia_lavorazione=tipologia_lavorazione, settore=settore)

            AssistenzaLavorazione.addRow(new)

    def eliminaAssistenza(nome):

        AssistenzaLavorazione.query.filter_by(nome=nome).update({'nome': '', 'costo': 0})
        AssistenzaLavorazione.commit()

    def modificaAssistenza(nome, tipologia_lavorazione, settore, modifica):
        AssistenzaLavorazione.query.filter_by(nome=nome, tipologia_lavorazione=tipologia_lavorazione,
                                              settore=settore).update(modifica)
        AssistenzaLavorazione.commit()

    def modificaNomeAssistenzaGenerale( old_nome, new_nome):
        AssistenzaLavorazione.query.filter_by(nome=old_nome).update({'nome': new_nome})
        AssistenzaLavorazione.commit()

    def returnAssistenzeDistinte():

        assistenze = AssistenzaLavorazione.query.all();

        assistenzeDistinte = []


        for assistenza in assistenze:
            if assistenza.nome not in assistenzeDistinte:
                assistenzeDistinte.append(assistenza.nome)


        return assistenzeDistinte



