from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface

class ImpegniDBmodel(DbUSinterface, DbUSinterface.db.Model):
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
    checkato = Column(Boolean())

