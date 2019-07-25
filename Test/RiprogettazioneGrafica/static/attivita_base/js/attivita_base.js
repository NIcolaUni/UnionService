class AttivitaBase extends OggettoBase {
    constructor(oggettoGeneratore, $where_to_append){
        super($('<div class="col-md-2 d-md-block d-sm-none  col-left"> \
                    <div id="base_activity_container" class="container-fluid"> \
                        <div id="base_activity_slider_wrapper" class="slider-wrapper"> \
                        </div> \
                    </div> \
                </div>'), oggettoGeneratore, $where_to_append);


        this.activity_list = [];
        this.height_pagine = 0;


    }

    popolaActivityList(){

        var $space_btns = this.referenzaDOM.children('#base_activity_container').children('#base_activity_slider_wrapper');

        this.activity_list.push( new Note_btn(this, $space_btns, this.padre.note_page) );
        this.activity_list.push( new Agenda_btn(this, $space_btns, this.padre.agenda_page) );
        this.activity_list.push( new Calendario_btn(this, $space_btns, this.padre.calendario_page) );
        this.activity_list.push( new Gestione_dip_btn(this, $space_btns, this.padre.gestione_dip_page) );
        this.activity_list.push( new Accogli_cliente_btn(this, $space_btns, this.padre.accogli_cliente_page) );
        this.activity_list.push( new Email_btn(this, $space_btns, this.padre.email_page) );

        this.abilitaBottoni();
    }


    abilitaBottoni(){

        this.height_pagine = $('.activity_container').first().height();

        $('#sezione_presentazione').css('height', 'auto');
        $('.activity_container').css('height', this.height_pagine+'px');


        var cambiaPagina = function( height_pagine, activity_btn_selected ){

            var mostraActivityContainer = function(){
                $('.activity_container').each(function(){
                    $(this).css('visibility', 'visible');
                });
            }

            var nascondiActivityContainerNonAttivi = function(){
                $('.activity_container').each(function(){
                    if( $(this).attr('id') != activity_btn_selected.paginaAssociata.referenzaDOM.attr('id') )
                        $(this).css('visibility', 'hidden');
                });

            }

            var id_selezionato = activity_btn_selected.paginaAssociata.id_in_slider;

            var id_corrente = activity_btn_selected.padre.padre.attivita_corrente.id_in_slider;
            var id_referenzaDOM = activity_btn_selected.padre.padre.attivita_corrente.referenzaDOM.attr('id');

            mostraActivityContainer();


            if( id_corrente > id_selezionato ){

                var offset = id_corrente-id_selezionato;
                var spostamento = offset*height_pagine;
                $('#sezione_presentazione' ).animate({'margin-top': '+='+spostamento+'px'}, 300, nascondiActivityContainerNonAttivi);
              //  $('#note_activity_container').hide();
            }
            else if( id_corrente < id_selezionato ){

                var offset = id_selezionato-id_corrente;
                var spostamento = offset*height_pagine;
                $('#sezione_presentazione').animate({'margin-top': '-='+spostamento+'px'}, 300, nascondiActivityContainerNonAttivi);
                //$('#note_activity_container').hide();

            }
            else{
               // alert('non faccio niente')
               nascondiActivityContainerNonAttivi();
            }

            activity_btn_selected.padre.padre.attivita_corrente = activity_btn_selected.paginaAssociata;


            $.each(activity_btn_selected.padre.activity_list, function(index, activity){
                activity.paginaDisattiva();
            });

            activity_btn_selected.paginaAttiva();
          /*  */


        }

        var height_pagine = this.height_pagine;

        $.each(this.activity_list, function(index, activity){
            activity.abilitaBottone(cambiaPagina, height_pagine)
        });



    }



}