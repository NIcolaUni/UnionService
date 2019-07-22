class PreventivoGenerico{

    constructor(nomiColonna, intestazioneSettore, grandezzeCelle, listaColonneVisibili,
                    listaOptionsSelects, listaNomiElementi, listaIdSettoriPerElementi){

        this.tabellaPreventivo = TabellaPreventivo(nomiColonna, intestazioneSettore, grandezzeCelle, listaColonneVisibili, this);
        this.pannelloControllo = PannelloControllo(listaOptionsSelects, listaNomiElementi, listaIdSettoriPerElementi, this)
        this.celleNascoste = false;

    }

    hideShowCelleNascoste(){
        $.each( this.tabellaPreventivo.settoriTabella, function(index, settore){
            this.celleNascoste = !this.celleNascoste;
            settore.hideShowCelleNascoste(this.celleNascoste);

        });
    }

}