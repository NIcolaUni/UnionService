class PannelloControllo extends ElementoPannelloControllo{

    constructor(listaOptionsSelects, listaNomiElementi, listaIdSettoriPerElementi, oggettoGeneratore){
        /*
            - listaOptionsSelects: lista di liste; ogni lista elemento ha la forma [ str, [] ] dove:
                                    -str: titolo del selectElement
                                    -[]: lista di valori per le option del select associato ( quello indicato da str )

            si considerano le varie liste già ordinate secondo l'ordine di visualizzazione;

             - listaIdSettoriPerElementi: lista di liste;  l'elemento lista, è una lista coi valori degli id dei settori ordinati per posizione;

             al elemento listaNomiElementi[i] corrisponde l'id_settori in listaIdSettoriPerElementi[i];
        */

        super($('<div id="divFattura" class="features row"></div>'), oggettoGeneratore);
        this.listaSelectElement = [];


        $.each(listaOptionsSelects, function(index, el){
            var nuovoSelect = new SelectTipologiaElemento(index, el[0], el[1], this );
            this.listaSelectElement.push(nuovoSelect);

            this.referenzaDom.append(nuovoSelect);

        });


        this.pannelloRisultatiSelect = new PannelloRisultatiSelect(listaNomiElementi, listaIdSettoriPerElementi, this);

        this.referenzaDom.append(this.pannelloRisultatiSelect);

        this.idSelectsAttivi = [];

        $.each(this.listaSelectElement, function(index, selectEl){
            this.idSelectsAttivi.push(0);
        });

        this.avvisoCambiamentoSelect();
    }

    modificaListaSelectElemento(index, val){
        this.listaSelectElement[index] = val;

        this.avvisoCambiamentoSelect();
    }

    avvisoCambiamentoSelect(){
        this.pannelloRisultatiSelect.mostraBottoniSelezionati(this.idSelectsAttivi);
    }

    aggiungiElemento(nomeSettore, datiCelle, tipoDatoCelle){
        this.padre.tabellaPreventivo.aggiungiRiga(nomeSettore, datiCelle, tipoDatoCelle);

    }




}