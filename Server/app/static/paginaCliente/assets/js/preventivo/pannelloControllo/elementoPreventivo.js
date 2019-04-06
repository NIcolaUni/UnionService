class ElementoPreventivo{

    constructor(id, titoloElemento, idSelectsAssociati){
        this.id = id;
        this.visibile = true;
        this.idSelectsAssociati = idSelectsAssociati; // lista: numero di posizione di cella corrisponde all'id di uno specifico select, ogni valore all'id delle options del select

        var stringaIdSelects = '';

        $.each( this.idSelectsAssociati, function(index, idSelect){

            if( index+1 == this.idSelectsAssociati.length)   //se sono all'ultimo
                stringaIdSelects += idSelectsAssociati;
            else
                stringaIdSelects += idSelectsAssociati + '-';
        });


        this.referenzaDOM = $('<li>'+
                                '<button id="'+stringaIdSelects+'_elementoPreventivo-'+this.id+'" class="elementFattura">'+
                                    '<label for="'+stringaIdSelects+'_elementoPreventivo-'+this.id+'">'+titoloElemento+'</label>'+
                                '</button>'+
                              '</li>');
    }

    hideShowBottone(nascondi){

        if( nascondi )
            this.referenzaDOM.hide();
        else
            this.referenzaDOM.show();
    }

}