from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean
from app import database


class DirigenteDBmodel(database.Model):
    __tablename__ = "dirigente"
    username = Column(String(60), ForeignKey('dipendente.username', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True, nullable=False)

    def commitRegistrazione(dirigente):
        database.session.add(dirigente)
        database.session.commit()