class PreventivoGenerico{

    constructor(nomiColonna, intestazioneSettore, grandezzeCelle, listaColonneVisibili){
        this.tabellaPreventivo = TabellaPreventivo(nomiColonna, intestazioneSettore, grandezzeCelle, listaColonneVisibili);
        this.celleNascoste = false;
    }

    hideShowCelleNascoste(){
        $.each( this.tabellaPreventivo.settoriTabella, function(index, settore){
            this.celleNascoste = !this.celleNascoste;
            settore.hideShowCelleNascoste(this.celleNascoste);

        });
    }

}