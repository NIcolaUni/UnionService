from app import database

class DbUSinterface():
    '''
    Interfaccia database US. Sarebbe opportuno che tutte le classi la cui denominazione
     ha questa la forma *DBmodel.py la ereditino.
    '''
    db = database

    def rollback():
        database.session.rollback()

    def commit():
        database.session.commit()

    def addRow(row):
        database.session.add(row)
        DbUSinterface.commit()

    def addRowNoCommit(row):
        database.session.add(row)

    def delRow(row):
        database.session.delete(row)
        DbUSinterface.commit()