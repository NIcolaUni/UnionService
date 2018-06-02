from sqlalchemy import Column, String, ForeignKey, Date, Integer, Boolean, ForeignKeyConstraint, PrimaryKeyConstraint
from .dbUSinterface import DbUSinterface


class ModalitaPagamentoFornitoreDBmodel(DbUSinterface, DbUSinterface.db.Model):
    __tablename__ = "modalita_pagamento_fornitore"
    __table_args__ = (
            PrimaryKeyConstraint('nome'),
            )
    nome = Column(String(150))