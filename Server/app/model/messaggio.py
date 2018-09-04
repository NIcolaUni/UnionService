from .db.messaggioDBmodel import MessaggioDBmodel
from .dipendente import Dipendente
from operator import  attrgetter
import datetime, app

class Messaggio(MessaggioDBmodel):

    def __init__(self, mittente, destinatario, testo, data, ora):
        self.mittente=mittente
        self.destinatario=destinatario
        self.testo=testo
        self.data=data
        self.ora=ora


    def registraMessaggio( mittente, destinatario, testo ):

        now =datetime.datetime.now()
        dip=Dipendente.query.filter_by(username=mittente).first()

        data = "{}/{}/{}".format(now.date().day, now.date().month, now.date().year)
        ora = "{}:{}:{}".format(now.time().hour, now.time().minute, now.time().second)

        msg = Messaggio(mittente=mittente, destinatario=destinatario, testo=testo, data=now.date(), ora=now.time())

        MessaggioDBmodel.addRow(msg)

        msgForDestHtml = '<div class="bubble"><div class="txt"><p class="name">{} {}</p>'.format(dip.nome, dip.cognome)+ \
                                '<p class="message">{}</p><br/>'.format(testo) + \
                                '<span class="timestamp">{} - {}</span>'.format(data, ora) + \
                                '</div><div class="bubble-arrow"></div></div>';

        return ((now.date(), now.time()), msgForDestHtml)

    def ordinaConversazioni(conversazioni):

        return sorted(conversazioni, key=attrgetter('data', 'ora'))

    def recuperaConversazioni(mittente, destinatario):


        mittenteMsg = MessaggioDBmodel.query.filter_by(mittente=mittente, destinatario=destinatario).all()

        destinatarioMsg = MessaggioDBmodel.query.filter_by(mittente=destinatario, destinatario=mittente).all()


        messaggi_ordinati = Messaggio.ordinaConversazioni(conversazioni=mittenteMsg+destinatarioMsg)

        storicoMsgHtml = ""

        for msg in messaggi_ordinati:
            app.server.logger.info('primo {}'.format(msg))

        for msg in messaggi_ordinati:

            app.server.logger.info(msg)


            data = "{}/{}/{}".format(msg.data.day, msg.data.month, msg.data.year)
            ora = "{}:{}:{}".format(msg.ora.hour, msg.ora.minute, msg.ora.second)

            if msg.mittente == mittente:

                storicoMsgHtml+='<div class="bubble alt"><div class="txt"><p class="name alt">Io</p>'+ \
                                '<p class="message">{}</p><br/>'.format(msg.testo) + \
                                '<span class="timestamp">{} - {}</span>'.format(data, ora) + \
                                '</div><div class="bubble-arrow alt"></div></div>'

            else:
                storicoMsgHtml += '<div class="bubble"><div class="txt"><p class="name">{}</p>'.format(msg.mittente) + \
                                  '<p class="message">{}</p><br/>'.format(msg.testo) + \
                                  '<span class="timestamp">{} - {}</span>'.format(data, ora) + \
                                  '</div><div class="bubble-arrow"></div></div>'

        return storicoMsgHtml