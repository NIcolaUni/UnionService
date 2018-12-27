from sqlalchemy import Column, String, ForeignKey, Float, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class PagamentiClienteDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "pagamenti_cliente"
    __table_args__ = (
            PrimaryKeyConstraint('numero_preventivo'),
                    )

    numero_preventivo = Column(Integer())
    totale_prev_edile = Column(Float(), default=0)
    totale_prev_finiture = Column(Float(), default=0)
    totale_prev_varianti = Column(Float(), default=0)
    acconto = Column(Float(), default=0)
    acconto_pagato = Column(Boolean())
    prima_rata = Column(Float(), default=0)
    prima_rata_pagata = Column(Boolean(), default=False)
    seconda_rata =  Column(Float(), default=0)
    seconda_rata_pagata = Column(Boolean(), default=False)
    terza_rata = Column(Float(), default=0)
    terza_rata_pagata = Column(Boolean(), default=False)
    saldo = Column(Integer(), default=0)
    saldo_pagato = Column(Boolean(), default=False)


