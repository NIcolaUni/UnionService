
class SettoreTabella extends ElementoTabella{

    constructor(id, nomeSettore, intestazioneSettore, oggettoGeneratore){

        super($('<tbody class="settore-'+id+'"></tbody>'), oggettoGeneratore);

        this.id = id;
        this.referenzaDOMIntestazioneSettore = $('<thead class="settore-'+id+'">'+
                                                    '<tr class="trHead intestazioneSettore">'+intestazioneSettore+'</tr>'+
                                                    '<tr class="trHead legendaSettore"></tr>'+
                                                 '</head>');
        this.nomeSettore = nomeSettore;
        this.righeSettore = [];

        this.generaColonneLegenda();
    }

    generaColonneLegenda(){

        $.each(this.padre.nomiColonna, function(index, nome){
            var nuovaCella = $('<th>'+nome+'</th>');
            this.referenzaDOMIntestazioneSettore.children('tr.legendaSettore').append(nuovaCella);
            nuovaCella.css('width', this.padre.grandezzeCelle[index]);
        });
    }

    aggiungiRiga(datiCelle, tipoDatoCelle){

        var nuovaRiga = RigaPrimaria(this.righeSettore.length, datiCelle, tipoDatoCelle, this);

        this.righeSettore.push(nuovaRiga);
        this.referenzaDOM.append(nuovaRiga);

    }

    hideShowCelleNascoste(nascondi){
        /*
            il parametro nascondi è un booleano
        */
        $.each(this.righeSettore, function(index, riga){
            $.each( riga.listaCelle, function(index, cella){
                cella.nascondiCella(nascondi);
            });
        });
    }


    riordinaRighe(){

    }

}
