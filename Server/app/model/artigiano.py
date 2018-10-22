from .db.artigianoDBmodel import ArtigianoDBmodel


class Artigiano(ArtigianoDBmodel):

    def __init__(self, nominativo, impiego, valutazione=0, contatti1=None, contatti2=None, email=None, note=None):
        self.nominativo = nominativo
        self.impiego = impiego
        self.valutazione = valutazione
        self.contatti1 = contatti1
        self.contatti2 = contatti2
        self.email = email
        self.note = note


    def registraArtigiano( nominativo, impiego, valutazione=0, contatti1=None, contatti2=None, email=None, note=None ):


        newArt = ArtigianoDBmodel(nominativo=nominativo, impiego=impiego, valutazione=valutazione,
                                  contatti1=contatti1, contatti2=contatti2,
                                    email=email, note=note)

        ArtigianoDBmodel.addRow(newArt)

    def eliminaArtigiano(nominativo, impiego):

        toDel =  ArtigianoDBmodel.query.filter_by(nominativo=nominativo, impiego=impiego).first()
        ArtigianoDBmodel.delRow(toDel)

    def modificaArtigiano(nominativo, impiego, modifica):

        ArtigianoDBmodel.query.filter_by(nominativo=nominativo, impiego=impiego).update(modifica);

        ArtigianoDBmodel.commit()

    def modificaColore(nominativo, impiego, colore):

        Artigiano.modificaArtigiano(nominativo=nominativo, impiego=impiego, modifica={'colore':colore})