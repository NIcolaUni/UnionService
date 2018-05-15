from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from app import database


class ImpegniDBmodel(database.Model):
    __tablename__ = "impegni"
    __table_args__ = (
            PrimaryKeyConstraint('dipendente', 'id'),
            ForeignKeyConstraint(['dipendente'], ['dipendente.username'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
            ForeignKeyConstraint(['dirigente'], ['dirigente.username'],
                                 onupdate="CASCADE", ondelete="CASCADE")
                    )
    dipendente = Column(String(60))
    id = Column(Integer)
    testo = Column(String(500), nullable=False)
    dirigente = Column(String(60))

    def commitImpegni(impegno):

        database.session.add(impegno)
        database.session.commit()

    def eliminaImpegni(impegno):
        database.session.delete(impegno)
        database.session.commit()