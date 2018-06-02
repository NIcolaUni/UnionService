from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class GiorniPagamentoFornitoreDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "giorni_pagamento_fornitore"
    __table_args__ = (
            PrimaryKeyConstraint('nome'),
            )
    nome = Column(String(150))