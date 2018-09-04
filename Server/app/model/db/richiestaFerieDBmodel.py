from sqlalchemy import Column, String, Date, Integer, ForeignKeyConstraint, Boolean, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class RichiestaFerieDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "richiesta_ferie"
    __table_args__ = (
        PrimaryKeyConstraint('dipendente', 'start_date'),

        ForeignKeyConstraint(['dipendente'], ['dipendente.username'],
                             onupdate='CASCADE', ondelete='CASCADE'),

    )

    dipendente = Column(String(60))
    titolo = Column(String(120))
    start_date = Column(Date())
    end_date = Column(Date())


