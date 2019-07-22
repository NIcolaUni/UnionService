class NoteDipendente extends OggettoBase {
    constructor(oggettoGeneratore){
        super($('<div id="note_container"> \
                    <div id="note_title" class="row"> \
                        <h3>NOTE del GIORNO</h3> \
                    </div> \
                    <div id="note_content" class="row">\
                    </div>'), oggettoGeneratore);
        this.nome='sono il padre'
        this.note = [];
        this.areaAggiungiNota = null;
        this.corpoListaNote = null;
        this.costruisciCorpoListaNote();
        this.costruisciAreaAggiungiNota();

        this.areaAggiungiNota.referenzaDOM.appendTo(this.referenzaDOM.children('#note_content'));
        this.corpoListaNote.appendTo(this.referenzaDOM.children('#note_content'));
    }

    costruisciAreaAggiungiNota(){
        var setta_note = new SettaNote(this, ['gigi', 'marco']);

        this.areaAggiungiNota = setta_note;

    }

    costruisciCorpoListaNote(){

        var corpoListaNote = $('<div id="area_note_registrate"></div>');
        this.corpoListaNote = corpoListaNote;
    }

    equindi(){

        alert('equindi')
    }

    eliminaNota(id){


        var tmp = []
        $.each(this.note, function(index, nota){
            if(nota.id != id){
                tmp.push(nota);
            }

        });

        $('#nota_dip_'+id).remove();

        this.aggiornaIds(tmp);

        this.note = tmp;


    }

    aggiornaIds(listaNote){

    /* usato quando viene eliminata una nota; rienumera in ordine sequenziale tutta la lista di note */

        var counter = 0;

        $.each(listaNote, function(index, note){
            note.id = counter;
            counter++;
        });

        /*ridenominazione ids oggetti DOM per evitare id uguali*/
        $('.nota_dipendente').each(function(){
            var old_id=$(this).attr('id');
            $(this).attr('id', old_id+'_old');

            var $checkbox_container = $(this).children('.checkbox_area').children('.checkbox_container');

            old_id = $checkbox_container.children('input').attr('id');
            $checkbox_container.children('input').attr('id', old_id+'_old');

        });

        counter =0;

        /*assegnazione nuovi ids*/
        $('.nota_dipendente').each(function(){

            $(this).attr('id', 'nota_dip_'+counter);
            var $checkbox_container = $(this).children('.checkbox_area').children('.checkbox_container');

            $checkbox_container.children('input').attr('id', 'nota_'+counter);
            $checkbox_container.children('label').attr('for', 'nota_'+counter);
            counter++;
        });


    }

    aggiungiNota(messaggio, personale, dirigente){ //il parametro "personale" e' un booleano; il parametro dirigente è
                                                   // null se personale vale true;

        var lastId = -1;

        if( this.note.length > 0 ){
            lastId = parseInt(this.note.slice(-1)[0].id);

        }


        var nota = null;

        if( personale ){
            nota = new NotaPersonale( this, messaggio,lastId+1);


        }
        else{
            nota = new NotaDirigente( this, messaggio, lastId+1, dirigente);
        }

        nota.referenzaDOM.appendTo(this.corpoListaNote);

        this.note.push(nota);

    }

}