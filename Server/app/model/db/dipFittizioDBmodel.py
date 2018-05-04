from sqlalchemy import String, Column, Boolean, ForeignKey, ForeignKeyConstraint
from app import database


class DipFittizioDBmodel(database.Model):
    __tablename__="dipendente_fittizio"
    __table_args__ = (
            ForeignKeyConstraint(['username', 'password'], ['dipendente_registrato.username', 'dipendente_registrato.password'],
                                 onupdate="CASCADE", ondelete="CASCADE"),
                    )

    username = Column(String(30),  primary_key=True )
    password = Column(String(30), nullable=False)
    classe = Column(String(20), nullable=False)
    dirigente = Column(Boolean, nullable=False)
    creatoreCredenziali = Column(String(60), ForeignKey('dirigente.username',  onupdate="CASCADE", ondelete="CASCADE"))
