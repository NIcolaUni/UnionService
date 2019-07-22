class ElementoPreventivo extends ElementoPannelloControllo{

    constructor(id, titoloElemento, idSelectsAssociati, datiAssociati, tipoDati, oggettoGeneratore){
        super($('<li>'+
                    '<button id="'+stringaIdSelects+'_elementoPreventivo-'+this.id+'" class="elementoPreventivo">'+
                        '<label for="'+stringaIdSelects+'_elementoPreventivo-'+this.id+'">'+titoloElemento+'</label>'+
                    '</button>'+
                '</li>'), oggettoGeneratore);
        this.id = id;
        this.visibile = true;
        this.idSelectsAssociati = idSelectsAssociati; // lista: numero di posizione di cella corrisponde all'id di uno specifico select, ogni valore all'id delle options del select
        this.titoloElemento = titoloElemento;
        this.datiAssociati = datiAssociati;
        this.tipoDati = tipoDati;
        this.inserito = false;

        var stringaIdSelects = '';

        $.each( this.idSelectsAssociati, function(index, idSelect){

            if( index+1 == this.idSelectsAssociati.length)   //se sono all'ultimo
                stringaIdSelects += idSelectsAssociati;
            else
                stringaIdSelects += idSelectsAssociati + '-';
        });

        this.referenzaDOM.children('button.elementoPreventivo').click(function(){

            this.inserisciElementoInPreventivo();
        });

    }

    hideShowBottone(nascondi){

        if( nascondi )
            this.referenzaDOM.hide();
        else
            this.referenzaDOM.show();
    }

    inserisciElementoInPreventivo(){
        if( !this.inserito ){

            this.inserito = true;
            this.padre.padre.aggiungiElemento(this.titoloElemento, this.datiAssociati, this.tipoDati);
        }
    }

}