class NotaPersonale extends NotaBase {
    constructor( oggettoGeneratore, messaggio, idNota){
        super($('<div id="nota_dip_'+idNota+'" class="nota_personale nota_dipendente"> \
                    <div class="checkbox_area_personale checkbox_area"> \
                        <div class="checkbox_container"> \
                        </div> \
                    </div> \
                    <div class="messaggio_nota_container"> \
                    </div> \
                 </div>'), oggettoGeneratore, messaggio, idNota);


        var $checkbox_grafica = $('<label class="checkbox_note" for="nota_'+idNota+'"></label>');
        var $checkbox_container = this.referenzaDOM.children('.checkbox_area_personale').children('.checkbox_container');

        this.labelMessaggioNota.appendTo(this.referenzaDOM.children('.messaggio_nota_container'));
        this.checkbox.appendTo($checkbox_container);
        $checkbox_grafica.appendTo($checkbox_container);

        this.aggiungiDelNotaBtn();

    }


}