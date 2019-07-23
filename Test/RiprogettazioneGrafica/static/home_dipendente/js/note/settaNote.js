class SettaNote extends OggettoBase {
    constructor(oggettoGeneratore, $where_to_append, listaDipendenti ){ //listaDipendenti è vuota in caso il dipendente non sia anche dirigente
        super($('<div id="addNotaBtn"> \
                    <a class="fa fa-plus"></a> \
                    <div id="componi_nota" style="display:none"> \
                    </div> \
                 </div>'), oggettoGeneratore, $where_to_append);

        this.annulla_nota_btn = $('<div id="annulla_nota" class="control_button_destinatario_note"><a class="fa fa-close" style="color:red"></a></div>');
        this.conferma_nota_btn = $('<div id="conferma_nota" class="control_button_destinatario_note"><a class="fa fa-check" style="color:green"></a></div>');

        this.textarea_settaNote = null;
        this.select_dipendenti = null;

        this.dirigente = false;

        if( listaDipendenti.length > 0 )
            /* attributo a true se il dipendente utente è anche un dirigente */
            this.dirigente = true;

        this.costruisciAreaDiComposizioneNote();
        this.costruisciAreaSelezioneDestinatario(listaDipendenti);

        var thisRef = this;



        this.referenzaDOM.click( function(){
            thisRef.apriAggiungiNota();
        });




        this.annulla_nota_btn.click(function(){

            thisRef.chiudiComposizioneNota(thisRef);

        });

        this.conferma_nota_btn.click(function(){
            thisRef.confermaInvioNota();
        });


    }


    apriAggiungiNota(){


        this.referenzaDOM.children('a').hide();
        this.referenzaDOM.children('div#componi_nota').show();

        this.referenzaDOM.css({
            "width": "calc(100% - 47px)",
            "height": "calc(100% - 25px)",
            "border-radius": "2px",
            "top": "0",
            "z-index": "1",
            "box-shadow": "0 5px 8px rgba(0, 0, 0, 0.2)",
            "max-height": "300px",
            "overflow": "visible",
            "position": "relative",
            "margin": "0 auto",
            "right": "0",
            "cursor": "auto"
        });

        this.padre.corpoListaNote.css('margin-top', '-43%');

        this.referenzaDOM.unbind('click');
    }

    chiudiComposizioneNota(settaNoteRef){
        this.referenzaDOM.children('a').show();
        this.referenzaDOM.children('div#componi_nota').hide();
        this.referenzaDOM.attr('style', '');
        this.padre.corpoListaNote.css('margin-top', '7%');

        this.textarea_settaNote.val('');

        this.referenzaDOM.click(function(){
            settaNoteRef.apriAggiungiNota(settaNoteRef);

        });


        event.stopImmediatePropagation()
    }

    confermaInvioNota(){
        var testo = this.textarea_settaNote.val();

        if( this.select_dipendenti.val() == 'personale' ){

            this.padre.aggiungiNota( testo, true, null);
        }
        else
            this.padre.aggiungiNota( testo, false, this.select_dipendenti.val());

        this.chiudiComposizioneNota(this);
    }

    costruisciAreaDiComposizioneNote(){
        var textareaNote = $('<textarea id="textarea_nota" placeholder="Testo..."></textarea>');
        var containerTextarea = $('<div id="container_textarea_nota" class="row"></div>');

        textareaNote.hover(function(){textareaNote.focus()});

        textareaNote.appendTo(containerTextarea);

        containerTextarea.appendTo(this.referenzaDOM.children('#componi_nota'));

        this.textarea_settaNote = textareaNote;


    }

    costruisciAreaSelezioneDestinatario(listaDipendenti){

        var select_dip = $('<select id="select_destinatario_nota"><option>personale</option></select>');

        var areaSelezioneDestinatario = $('<div id="area_destinatario_nota" class="row"> \
                                                <div id="container_select_destinatario_nota"> \
                                                </div> \
                                                <div id="control_area_destinatario_nota"> \
                                                </div> \
                                            </div>');

        this.annulla_nota_btn.appendTo(areaSelezioneDestinatario.children('#control_area_destinatario_nota'));
        this.conferma_nota_btn.appendTo(areaSelezioneDestinatario.children('#control_area_destinatario_nota'));

        $.each(listaDipendenti, function(index, dip){
            $('<option>'+dip+'</option>').appendTo(select_dip);
        });

        select_dip.appendTo(areaSelezioneDestinatario.children('#container_select_destinatario_nota'));

        areaSelezioneDestinatario.appendTo(this.referenzaDOM.children('#componi_nota'));

        this.select_dipendenti = select_dip;

        if( listaDipendenti.length == 0 ){
            this.select_dipendenti.hide();

        }

    }
}