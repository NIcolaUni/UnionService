from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class SettoreLavorazioneDBmodel(database.Model):
    __tablename__ = "settore_lavorazione"
    __table_args__ = (
        ForeignKeyConstraint(['categoria'],
                             ['categoria_lavorazione.nome'],
                             onupdate="CASCADE", ondelete="SET NULL"),
        ForeignKeyConstraint(['pertinenza'],
                             ['pertinenza_lavorazione.nome'],
                             onupdate="CASCADE", ondelete="SET NULL")
        )

    nome = Column(String(100), primary_key=True)
    categoria = Column(String(100))
    pertinenza = Column(String(100))

    def commitSettore(nuovoSettore):
        database.session.add(nuovoSettore)
        database.session.commit()

    def commitEliminaSettore(settore):
        database.session.delete(settore)
        database.session.commit()