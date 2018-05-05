from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint
from app import database


class NotificaDBmodel(database.Model):
    __tablename__ = "notifica"
    __table_args__ = (
            PrimaryKeyConstraint('dipendente', 'titolo'),

            )

    dipendente = Column(String(60), ForeignKey('dipendente.username',  onupdate="CASCADE", ondelete="CASCADE"))
    titolo = Column(String(60))
    contenuto = Column(String(500))

    def commitNotifica(notifica):
        database.session.add(notifica)
        database.session.commit()