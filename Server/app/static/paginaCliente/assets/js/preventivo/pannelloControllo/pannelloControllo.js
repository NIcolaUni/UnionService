class PannelloControllo{

    constructor(listaOptionsSelects){
        /*
            - listaOptionsSelects: lista di liste; ogni lista elemento ha la forma [ str, [] ] dove:
                                    -str: titolo del selectElement
                                    -[]: lista di valori per le option del select associato ( quello indicato da str )

            si considerano le varie liste già ordinate secondo l'ordine di visualizzazione;
        */

        this.listaSelectElement = [];
        this.listaElementiPreventivo = [];

        this.referenzaDom = $('<div id="divFattura" class="features row"></div>');

        $.each(listaOptionsSelects, function(index, el){
            var nuovoSelect = new SelectTipologiaElemento(index, el[0], el[1] );
            this.listaSelectElement.push(nuovoSelect);

            this.referenzaDom.append(nuovoSelect);

        });
    }

}