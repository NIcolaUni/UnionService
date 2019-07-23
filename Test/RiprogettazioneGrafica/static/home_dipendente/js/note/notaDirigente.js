class NotaDirigente extends NotaBase {
    constructor( oggettoGeneratore, $where_to_append, messaggio, idNota, dirigente){
        super($('<div id="nota_dip_'+idNota+'" class="nota_dirigente nota_dipendente"> \
                    <div class="checkbox_area_dirigente checkbox_area"> \
                        <div class="checkbox_container"> \
                        </div> \
                        <div class="nome_dirigente_note"> '+dirigente+': </div> \
                    </div> \
                    <div class="messaggio_nota_container"> \
                    </div> \
                 </div>'), oggettoGeneratore, $where_to_append, messaggio, idNota);

        this.idDirigente = true;
        this.dirigente = dirigente; //nome del dirigente



        var $checkbox_grafica = $('<label class="checkbox_note" for="nota_'+idNota+'"></label>');
        var $checkbox_container = this.referenzaDOM.children('.checkbox_area_dirigente').children('.checkbox_container');

        this.labelMessaggioNota.appendTo(this.referenzaDOM.children('.messaggio_nota_container'));
        this.checkbox.appendTo($checkbox_container);
        $checkbox_grafica.appendTo($checkbox_container);

        this.aggiungiDelNotaBtn();


    }


}