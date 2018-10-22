from sqlalchemy import Column, String, Date, Boolean, ForeignKeyConstraint, Integer
from .dbUSinterface import DbUSinterface
from app import database

class DipendenteDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "dipendente"
    __table_args__ = (
            ForeignKeyConstraint(['username', 'password'], ['dipendente_registrato.username', 'dipendente_registrato.password'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
                    )
    username = Column(String(60), primary_key=True, nullable=False)
    password =Column(String(30), nullable=False)
    cf = Column(String(16), unique=True, nullable=False)
    nome = Column(String(30), nullable=False)
    cognome = Column(String(30), nullable=False)
    dataNascita = Column(Date(), nullable=False)
    residenzaVia = Column(String(120), nullable=False)
    residenzaNum = Column(Integer(), nullable=False)
    residenzaCitta = Column(String(120), nullable=False)
    residenzaCap = Column(Integer())
    residenzaRegione = Column(String(120), nullable=False)
    domicilioVia = Column(String(120))
    domicilioNum = Column(Integer())
    domicilioCitta = Column(String(120))
    domicilioCap = Column(Integer())
    domicilioRegione = Column(String(120))
    telefono = Column(String(12), nullable=False)
    email_aziendale = Column(String(50), nullable=False)
    email_personale = Column(String(50))
    iban = Column(String(30))
    partitaIva = Column(String(30))
    classe = Column(String(30), nullable=False)
    dirigente = Column(Boolean, nullable=False)
    session_id = Column(String(40), unique=True, default=None)
    immagine_profilo = Column(String(500), default='senzaImmagine.jpg')


    def commitRegistrazione(dipFitReg, dipReg, dip):
        database.session.delete(dipFitReg)
        database.session.add(dipReg)
        database.session.commit()
        database.session.add(dip)
        database.session.commit()


