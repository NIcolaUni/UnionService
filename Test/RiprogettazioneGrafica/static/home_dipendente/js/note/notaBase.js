class NotaBase extends OggettoBase {
    constructor( referenzaDOM, oggettoGeneratore, $where_to_append, messaggio, idNota){
        super( referenzaDOM, oggettoGeneratore, $where_to_append);


        this.id = idNota //intero associato ad ogni nota aggiunta incrementando il valore dell'ultima nota registrata
        this.isDirigente = false;

        this.labelMessaggioNota = null;
        this.checkbox = null;

        var $labelMessaggio = $('<label class="messaggio_nota">'+messaggio+'</label>')
        var $checkbox_nascosta = $('<input class="hidden_checkbox_note" type="checkbox" id="nota_'+idNota+'" />');

        this.labelMessaggioNota = $labelMessaggio;
        this.checkbox = $checkbox_nascosta;

        this.eliminaNota = $('<div class="delNota"><a class="fa fa-close"></a></div>');

        var thisRef = this;

        this.checkbox.click(function(){
            thisRef.sottolineaNotaVisionata();
        });


    }

    aggiungiDelNotaBtn(){

        var thisRef = this;

        this.eliminaNota.click(function(){
            thisRef.padre.eliminaNota(thisRef.id);

        });

        this.eliminaNota.appendTo(this.referenzaDOM.children('.checkbox_area'));

    }


    sottolineaNotaVisionata(){

        if(this.checkbox.is(':checked'))
            this.labelMessaggioNota.css('text-decoration', 'line-through' );
        else
            this.labelMessaggioNota.css('text-decoration', 'none' );


    }

}