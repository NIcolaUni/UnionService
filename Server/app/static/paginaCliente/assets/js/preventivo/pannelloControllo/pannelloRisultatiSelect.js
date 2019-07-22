class PannelloRisultatiSelect extends ElementoPannelloControllo{

    constructor(listaNomiElementi, listaDatiElementi, listaTipoDatiElementi, listaIdSettori, oggettoGeneratore){
        /*
            listaDatiElementi: Contiene i dati extra necessari per aggiungere una riga;
                               ogni cella rappresenta un elementoPreventivo particolare ordinato come in "listaNomiElementi".
                               ogni elemento di cella è un array contenete l'informazione extra;
            listaIdSettori: lista di liste;  l'elemento lista, è una lista coi valori degli id dei settori ordinati per posizione;

            al elemento listaNomiElementi[i] corrisponde l'id_settori in listaIdSettori[i];
        */
        super($('<div  id="pannelloRisultati" class="features col-md-8">'+
                    '<ul id="listaRisultati"></ul>'+
                '</div>'), oggettoGeneratore);

        this.listaElementiPreventivo = [];

        popolaListaRisultati(listaNomiElementi, listaDatiElementi, listaIdSettori);

    }

    popolaListaRisultati(listaNomiElementi, listaDatiElementi, listaTipoDatiElementi, listaIdSettori){

        $.each(listaNomiElementi, function(index, nome){
            var nuovoBottone = new ElementoPreventivo(index, nome, listaIdSettori[index], listaDatiElementi, listaTipoDatiElementi, this);
            this.listaElementiPreventivo.push(nuovoBottone);
            this.referenzaDom.children('ul').append(nuovoBottone);
        });


    }

    mostraBottoniSelezionati(idSelectsSelezionati){
        // idSelectsSelezionati lista, ogni cella ha associato
        // un select e il valore della celle è l'option selezionato di quel select

        $.each(this.listaElementiPreventivo, function(index, elemento){

            var selectAssociato = true;

            $.each(elemento.idSelectsAssociati, function(index, idSelectElemento){
                if( idSelectElemento != idSelectsSelezionati(index) )
                    selectAssociato = false;

            });

            if( selectAssociato ){
                elemento.hideShowBottone(false);
            }
            else{
                elemento.hideShowBottone(true);
            }

        });

    }

}