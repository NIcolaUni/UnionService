from .db.dipFittizioDBmodel import DipFittizioDBmodel
from .dipendenteRegistrato import DipendenteRegistrato
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import app

class DipendenteFittizio(DipFittizioDBmodel):

    def __init__(self, username, password, classe, dirigente, creatoreCredenziali):
        self.username = username
        self.password = password
        self.classe = classe
        self.dirigente = dirigente
        self.creatoreCredenziali = creatoreCredenziali

    # Equivalente al toString() di java
    def __repr__(self):
        return "<DipendenteFittizio- {0}>".format(self.username)

    def registraDipendente( username, password, classe, dirigente, creatoreCredenziali):
        dipReg = DipendenteRegistrato(username=username, password=password, fittizio=True)
        newDipFittizio = DipendenteFittizio(username=username, password=password,
                                                classe=classe, dirigente=dirigente, creatoreCredenziali=creatoreCredenziali)

        DipFittizioDBmodel.commitRegistrazione(dipReg, newDipFittizio)

    class ThreadSendMail(threading.Thread):
        def __init__(self, email, username, password):
            threading.Thread.__init__(self)
            self.email = email
            self.username = username
            self.password = password

        def run(self):
            app.server.logger.info('\n\nSono il thread lanciato\n\n')
            msg = MIMEMultipart()
            msg["From"] = "pancheri.nicola@gmail.com"
            msg["To"] = self.email
            msg["Subject"] = "Credenziali d'accesso al gestionale"
            body = '''
                    Salve,
                    è stato autorizzato il suo accesso al gestionale UnionService.
                    Le sue credenziali sono:
                    username: {}
                    password: {}

                    Completi la registrazione all'indirizzo: http://192.168.1.135

                    '''.format(self.username, self.password)

            msg.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    # Next, log in to the server
                    server.login("pancheri.nicola@gmail.com", "fattiicazzituoi92")

                    # Send the mail
                    text = msg.as_string()
                    server.sendmail("pancheri.nicola@gmail.com", self.email, text)

            except:
                print("Errore: mail non inviata");
                raise

    def inviaCredenziali(email, username, password):

       newThread = DipendenteFittizio.ThreadSendMail( email, username, password )
       newThread.start()