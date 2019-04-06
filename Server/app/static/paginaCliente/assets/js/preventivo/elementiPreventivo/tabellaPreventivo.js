class TabellaPreventivo extends ElementoTabella{

    constructor(nomiColonna, intestazioneSettore, grandezzeCelle, listaColonneVisibili){
        /*
            Il parametro intestazioneSettore è una stringa html che non è altro la struttura
            html effettiva del intestazione del settore. Visto che può cambiare da preventivo
            a preventivo deve essere passata come parametro al momento della creazione
            della tabella. Nella pratica non è altro che un elenco di tag <th>; tra questi
            ve ne deve essere uno con classe nomeSettore;
        */
        super( $('<table id="bodyPreventivo"></table>'), null)

        this.nomiColonna = nomiColonna;
        this.grandezzeCelle = grandezzeCelle;
        this.listaColonneVisibili = listaColonneVisibili;
        this.numeroColonneVisibili = 0;
        this.numeroColonneNascoste = 0;
        this.intestazioneSettore = intestazioneSettore;
        this.settoriTabella = [];

        $.each(listaColonneVisibili, function(index, el){
            if(el)
                this.numeroColonneVisibili += 1;
            else
                this.numeroColonneNascoste += 1;
        });


    }

    aggiungiRiga(nomeSettore, datiCelle, tipoDatoCelle){

        var settorePresente = false;

        $.each(this.settoriTabella, function(index, settore){

           if(settore.nomeSettore == nomeSettore){
                settorePresente=true;
                settore.aggiungiRiga(datiCelle, tipoDatoCelle)
           }
        });

        if(!settorePresente){
            var id_settore=this.aggiungiSettore(nomeSettore);

            this.settoriTabella[id_settore].aggiungiRiga(datiCelle, tipoDatoCelle);

        }
    }

    aggiungiSettore(nomeSettore){
        var nuovoSettore = SettoreTabella(this.settoriTabella.length, nomeSettore=nomeSettore, this);
        this.settoriTabella.push(nuovoSettore);
        this.referenzaDOM.append(nuovoSettore.referenzaDOMIntestazioneSettore);
        this.referenzaDOM.append(nuovoSettore.referenzaDOM);

        return this.settoriTabella.length;
    }

    riordinaSettori(){

    }
}