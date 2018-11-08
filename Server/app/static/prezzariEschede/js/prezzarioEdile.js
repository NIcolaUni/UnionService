/*********************************************************************************************/
var filterZoneOpenWidthPerc = 60;
/*******************************************************************/
var riposizionaTabelle = function(){

}

/*****************************************************************************************************/
var lavorazioneInListaLavorazioni = function(lavorazione){

    var toAdd = true;

    $('#listaLavorazioni').children('option').each(function(){
        if( $(this).val() == lavorazione ){
            toAdd = false;
        }
    });

    if( toAdd ){
        $('#listaLavorazioni').append('<option>'+lavorazione+'</option>');
    }
}

/******************************************************************************************************/

var pulisciHeaderNewRow = function(){

    $('#headerNewRow input').each(function(){
        if( $(this).attr('type') == 'radio' )
            $(this).attr('checked', '' );
        else if($(this).hasClass('numInput'))
            $(this).val(0);
        else
        {
            $(this).val('');

        }
    });

    $('#headerNewRow td.fornituraPosa').children('label').html('&euro; 0');

    $('#headerNewRow textarea').each(function(){

        $(this).val('');

    });

}

/*****************************************************************************************************/

var verificaSettorePresente = function(settore, optionClass){

    var settorePresente=false;

    $('#listaSettori').children('option').each(function(){
        if( $(this).text() == settore )
            settorePresente = true;
    });

    if( !settorePresente ){

        if( settore != '' ){
            $('#selectPertinenzaNewRow').children('.tmpOption').remove();
            if( optionClass == "tmpOption" ){

                $('#selectPertinenzaNewRow').append('<option class="'+optionClass+'">'+ settore +'</option>');
            }
            else{
                $('#listaSettori').append('<option>'+ settore +'</option>');
                $('#modDelSettore').append('<option>'+ settore +'</option>');
                $('#selectPertinenzaNewRow').append('<option>'+ settore +'</option>');
            }
        }

    }



    $('#tabellaContainer td.pertinenza').each(function(){

        settorePresente=false;

        $(this).children('select').children('option').each(function(){
            if( $(this).text() == settore )
                settorePresente = true;
        });

        if( !settorePresente )
            $(this).children('select').append('<option>'+settore+'</option>');
    });

}

/****************************************************************************************************/

var hiddenInputAction = function($this){

    $('.inModifica').each(function(){
        $(this).removeClass('inModifica');
        $(this).children('label').show();
        $(this).children('input').hide();
        $(this).children('textarea').hide();
        $(this).children('label.simpleAfterInputLabel').hide();


    });


    $this.addClass('inModifica');
    $this.children('label').hide();
    $this.children('input').show();
    $this.children('textarea').show();
    $this.children('label.simpleAfterInputLabel').show();

}


/***************************************************************************************************/
var calcolaCostoFornituraPosa = function($row){

    var fornitura = parseFloat($row.children('td.fornitura').children('input').val());
    var posa = parseFloat($row.children('td.posa').children('input').val());

    var costo = fornitura + posa;

    costo = Math.round(costo*100)/100;

    $row.children('td.fornituraPosa').children('label').html('&euro; '+costo);

}

var aggiungiEventListenerCalcolaCosto = function($row){
    $row.children('td.fornitura').children('input').change(function(){
        calcolaCostoFornituraPosa($row);
    });

    $row.children('td.posa').children('input').change(function(){
        calcolaCostoFornituraPosa($row);
    });
}

/*************************************************************************************************/
/*se una sezione rimane senza lavorazione elimino il settore di lavorazione */


var verificaSettoreVuoto = function(){

        var eliminaSettore= function($this){
           var counter = 0;

           $this.children('tr').each(function(){
                counter++;

           });


           if( counter == 1 ){

            $this.remove();
           }

        }

        $('#tabellaContainer tbody').each(function(){
           eliminaSettore($(this));
        });


}


/*************************************************************************************************/

var cancellaRiga = function($row, usernameDip){

    var settore=$row.parent().attr('class');
    var tipo_lav=$row.children('td.tipologia_lavorazione').children('textarea').val();

    socketPrezzario.emit('elimina_lavorazione', {

        'dip': usernameDip,
        'settore': settore,
        'tipologia': tipo_lav

    });

    socketPrezzario.on('conferma_elimina_lav', function(){

        $row.remove();

        verificaSettoreVuoto();

    });

}


/************************************************************************************************/
/*
    Prende in input una riga dellaTabella e se la riga non ha la casse 'daVerificare'
    gliela aggiunge altrimenti gliela toglie; la modifica fatta viene poi segnalata
    al server tramite il segnale 'settaLavorazioneDaVerificare'
 */

var segnalaRiga = function($row){

        var settore = $row.parent().attr('class');
        var tipologia = $row.children('td.tipologia_lavorazione').children('textarea').val();
        var valore=false;


        if( $row.hasClass('daVerificare') ){
            $row.removeClass('daVerificare');
             $row.css('background', 'white');
        }
        else{
            $row.addClass('daVerificare');
            $row.css('background', 'yellow');
            valore=true;
        }

        socketPrezzario.emit('settaLavorazioneDaVerificare', {
            'settore': settore,
            'tipologia': tipologia,
            'valore': valore
        });

}

/*******************************************************************************************/
/*
Per ogni prezzario o schedario, la dimensione delle celle della tabella e del suo header
vengoro regolati col codice seguente;
*/

var tabellaSize = $(window).height()*65/100;

var regolaDimensioniHeader = function(idHeaderContainer, idTabellaContainer){

    $('.viewContainer').css( {height: tabellaSize+'px'});

    $('#'+idHeaderContainer).width( $('#'+idTabellaContainer).width()+1 );

    //Per ogni cella dell'header mi assicuro che le dimensioni corrispondano con le
    //celle della tabella contenente i dati

    var indexElement =0;
    var primaColSize = '9%;'

    $('#'+idHeaderContainer+' tbody').children('tr').each(function(){

        if( $(this).hasClass('headerDelHeader') ){
        //    alert('qua: '+$(this).attr('class'))

            $('this').children('td.primaCol').css('width', primaColSize );
        }
        else{

            $('#'+idTabellaContainer+' .sezioneTabella').children('td.primaCol').css('width', primaColSize );
          //  alert($(this).attr('class'))
            $(this).children('th').each(function(){

                if( $(this).hasClass('primaCol') ){
                    $(this).css('width', primaColSize)
                }
                else if( $(this).hasClass('tipologia_lavorazione') ||  $(this).hasClass('note') ){
                    $(this).css('width', '17%')

                }
                else if( $(this).hasClass('pertinenza') || $(this).hasClass('dimensione') ){
                    $(this).css('width', '14%')
                }
                else if( $(this).hasClass('numCellSmall') ){
                    $(this).css('width', '5%')

                }
                else if( $(this).hasClass('numCellBig') ){
                    $(this).css('width', '6%')

                }

            });

            $('#'+idTabellaContainer+' .datiScheda').children('td').each(function(){
                 if(!$(this).hasClass('tipologia')){

                    if( $(this).hasClass('primaCol') ){
                        $(this).css('width', primaColSize)
                    }
                    else if( $(this).hasClass('tipologia_lavorazione') ||  $(this).hasClass('note') ){
                        $(this).css('width', '17%')

                    }
                    else if( $(this).hasClass('pertinenza') || $(this).hasClass('dimensione') ){
                        $(this).css('width', '14%')
                    }
                    else if( $(this).hasClass('numCellSmall') ){
                        $(this).css('width', '5%')

                    }
                    else if( $(this).hasClass('numCellBig') ){
                        $(this).css('width', '6%')

                    }

                }

            });
        }
    });
}


/**************************************************************************************/

var aggiungiRiga = function(daVerificare, usernameDip){


    var $tbodyNewRow1=$('#tabellaContainerNewRow1').children('table').children('tbody');
    var $datiScheda1=$tbodyNewRow1.children('.datiScheda');
    var $sezioneTabella1=$tbodyNewRow1.children('.sezioneTabella');

    var $settore=$sezioneTabella1.children('th.primaCol').next('th').children('input');

    var $tipologia=$datiScheda1.children('td.tipologia_lavorazione').children('textarea');
    var $pertinenza=$datiScheda1.children('td.pertinenza').children('select');
    var $unita=$datiScheda1.children('td.unitaMisura').children('select');
    var $fornitura=$datiScheda1.children('td.fornitura').children('input');
    var $posa=$datiScheda1.children('td.posa').children('input');
    var $fornituraPosa=$datiScheda1.children('td.fornituraPosa').children('label').text().split(' ')[1];
    var $prezzoMin=$datiScheda1.children('td.prezzoMin').children('input');
    var prezzoMax=$datiScheda1.children('td.prezzoMax').children('input').val();
    var $dimensioni=$datiScheda1.children('td.dimensione').children('input');
    var $note=$datiScheda1.children('td.note').children('textarea');


    var $table=$('#tabellaContainer').children('table');

    if( prezzoMax == 0 ){
        prezzoMax = parseInt($fornitura.val())+parseInt($posa.val());

    }

    var tipoEsistente=false;

    $table.children('tbody').each(function(){
        if( $(this).attr('class') == $settore.val() ){
            tipoEsistente = true;
        }
    });

    if( !tipoEsistente ){
        $table.append(
            '<tbody class="'+$settore.val()+'"> \
                <tr class="sezioneTabella dimensionaTabella""> \
                    <th class="primaCol"></th> \
                    <th class="secondaCol" colspan="11">Settore di lavorazione: '+$settore.val()+'</th> \
                </tr> \
            <tbody>'
        );

    }
    var $tbodyToExpand=null;

    $table.children('tbody').each(function(){
        if( $(this).attr('class') == $settore.val() ){
            $tbodyToExpand=$(this);
        }
    });

    var tipologia = $tipologia.val().replace(/\n/g, "");
    var note = $note.val().replace(/\n/g, "");


    var datiSchedaNewRow=$(
                    '<tr class="datiScheda dimensionaTabella"> \
                        <td class="primaCol"><a class="fa fa-warning primaColIcon segnalaRow"></a><a class="fa fa-trash primaColIcon delRow"></a></td> \
                         <td class="tipologia" style="display:none"> \
                            <input class="inputScheda" value="'+tipologia+'"> \
                        </td> \
                        <td class="tipologia_lavorazione hiddenInput"><label class="cellaDato">'+tipologia+'</label> \
                            <textarea style="display:none" class="inputScheda" placeholder="tipologia lavorazione..." >'+tipologia+'</textarea>\
                        </td> \
                        <td class="pertinenza hiddenInput"> \
                            <select></select> \
                        </td> \
                        <td class="unitaMisura numCellBig">\
                            <select> \
                                <option>a corpo</option> \
                                <option>cad</option> \
                                <option>ml</option> \
                                <option>mq</option> \
                                <option>mc</option> \
                            </select> \
                        </td> \
                        <td class="fornitura hiddenInput numCellBig"><label class="cellaDato">&euro; '+$fornitura.val()+'</label> \
                           <label style="display:none" class="simpleAfterInputLabel">&euro;</label> <input type="number" step="0.01" style="display:none" class="inputScheda numInput"  value="'+$fornitura.val()+'"> \
                        </td> \
                        <td class="posa hiddenInput numCellSmall"><label class="cellaDato">&euro; '+ $posa.val()+'</label> \
                            <label style="display:none" class="simpleAfterInputLabel">&euro;</label> <input type="number" step="0.01" style="display:none" class="inputScheda numInput" value="'+ $posa.val()+'">  \
                        </td> \
                        <td class="fornituraPosa numCellSmall no_cursor"> \
                            <label class="cellaDato no_cursor">&euro; '+ $fornituraPosa +'</label> \
                        </td> \
                        <td class="prezzoMin hiddenInput numCellSmall"><label class="cellaDato">&euro; '+ $prezzoMin.val()+'</label> \
                            <label style="display:none" class="simpleAfterInputLabel">&euro;</label> <input type="number" step="0.01" style="display:none" class="inputScheda numInput" value="'+ $prezzoMin.val()+'"> \
                        </td> \
                        <td class="prezzoMax hiddenInput numCellSmall"><label class="cellaDato">&euro; '+ prezzoMax +'</label> \
                            <label style="display:none" class="simpleAfterInputLabel">&euro;</label> <input type="number" step="0.01"style="display:none" class="inputScheda numInput" value="'+ prezzoMax+'"> \
                        </td> \
                        <td class="dimensione hiddenInput"><label class="cellaDato">'+$dimensioni.val()+'</label> \
                            <input style="display:none" class="inputScheda" value="'+$dimensioni.val()+'" placeholder="dimensioni (LXHXP)..." > \
                        </td> \
                        <td class="note hiddenInput"><label class="cellaDato">'+note+'</label> \
                           <textarea style="display:none">'+note+'</textarea> \
                        </td> \
                    </tr>').appendTo($tbodyToExpand);

    lavorazioneInListaLavorazioni(tipologia);

    datiSchedaNewRow.children('td.unitaMisura').children('select').children('option').each(function(){
        if( $(this).text() == $unita.val() )
            $(this).attr('selected', 'selected');
    });

    datiSchedaNewRow.children('td.pertinenza').children('select').each(function(){
        $whereToAppend = $(this);

        $('#selectPertinenzaNewRow').children('option').each(function(){

            if( $(this).text() == $pertinenza.val() ){
               $whereToAppend.append('<option selected="selected">'+$(this).text()+'</option>');
            }
            else{
               $whereToAppend.append('<option>'+$(this).text()+'</option>');
            }

        });
    });

    datiSchedaNewRow.children('td.primaCol').children('a.delRow').click(function(){

        cancellaRiga(datiSchedaNewRow, usernameDip);
    });

    datiSchedaNewRow.children('td.primaCol').children('a.segnalaRow').click(function(){

        segnalaRiga(datiSchedaNewRow);
    });


    $('td.hiddenInput').click( function(){
        hiddenInputAction($(this));

    });


    var changeValueLavorazione = function($this){

        var $container=$this.parent();
        var $row = $container.parent();
        var settore = $row.parent().attr('class');
        var tipologia=$row.children('td.tipologia').children('input').val();

        var attributoToEdit=$container.attr('class').split(' ')[0];
        var valore = $this.val()

        if( attributoToEdit == 'note' ){
            valore= $this.val().replace( /\r?\n/gi, '');

        }


        socketPrezzario.emit('modifica_lavorazione',
            {
                'dip' : usernameDip,
                'settore' : settore,
                'tipologia' : tipologia,
                'toEdit' : attributoToEdit,
                'valore' : valore
            }
        );

        socketPrezzario.on('conferma_modifica_lavorazione', function(){


            $('.inModifica').each(function(){

                $(this).children('label').show();
                $(this).children('input').hide();
                $(this).children('textarea').hide();

                $(this).children('.simpleAfterInputLabel').hide();
                $(this).removeClass('inModifica');
            });


            if( $this.is('input') || $this.is('textarea') ){
                if( $container.hasClass('numCell') ){
                    if($container.hasClass('fornitura') || $container.hasClass('posa') ){
                        calcolaCostoFornituraPosa(datiSchedaNewRow);
                    }
                    $container.children('label.cellaDato').html('&euro; '+valore);
                }
                else{
                    $container.children('label.cellaDato').html(valore);
                }
            }

            if( attributoToEdit == 'tipologia_lavorazione' ){
                $row.children('td.tipologia').children('input').val(valore);
            }

        });


    }

    $('#tabellaContainer input').unbind('change').change(function(){

        changeValueLavorazione($(this));
    });

    $('#tabellaContainer textarea').unbind('change').change(function(){

        changeValueLavorazione($(this));
    });

    $('#tabellaContainer select').unbind('change').change(function(){
        changeValueLavorazione($(this));

    });


} // FINE AGGIUNGI RIGA

/****************************************************************************************/
var verificaPresenzaPertinenza= function($tbody, pertinenza){

    var countRow = 0;
    var countHiddenRow = 0;


    $tbody.children('tr.datiScheda').each( function(){
        var trPertinenza= $(this).children('td.pertinenza').children('select').val();

        countRow++;

        if( trPertinenza.startsWith(pertinenza) ){
            $(this).show();
        }
        else{
            countHiddenRow++;
            $(this).hide();
        }

    });

    if( countRow == countHiddenRow ){
        return false

    }

    return true;
}

var showAllRow = function($tabella){
    $tabella.children('table').children('tbody').each(function(){
        $(this).show();
        $(this).children('tr').show();
    });

}

var filtraTbody = function($tabella, classe){

    showAllRow($tabella);

    if( classe != '' ){
        $tabella.children('table').children('tbody').each(function(){
            var tbodyClass = $(this).attr('class');

            if( tbodyClass !== undefined ){

                tbodyClass = tbodyClass.toUpperCase();
                classe = classe.toUpperCase();

                if( !tbodyClass.startsWith(classe) ){

                    if(!verificaPresenzaPertinenza($(this), classe)){
                        $(this).hide();

                     }
                }
                else if( tbodyClass.startsWith(classe) ){

                    $(this).show();
                }

            }
        });
    }

}

/*******************************************************************************************/

var filtraRighe = function($tabella, tipologia){

    if( tipologia != '' ){

        $tabella.children('table').children('tbody').each(function(){

            var tbodyClass = $(this).attr('class');

            if( tbodyClass !== undefined ){
                var hideTbody = false;
                var countRow = 0;
                var countHiddenRow = 0;


                $(this).children('tr.datiScheda').each( function(){
                    var trTipologia= $(this).children('td.tipologia').children('input').val();

                    countRow++;

                    if( trTipologia.startsWith(tipologia) ){
                        $(this).show();
                    }
                    else{
                        countHiddenRow++;
                        $(this).hide();
                    }

                });

                if( countRow == countHiddenRow ){
                    $(this).hide();

                }
            }
        });

    }
    else{

        $tabella.children('table').children('tbody').each(function(){

            $(this).show();

            $(this).children('tr.datiScheda').each( function(){
                $(this).show();
            });


        });


    }

}

/**************************************************************************************/

var modificaRicaricoAziendale = function($input){

    socketPrezzario.emit('modifica_ricarico_prezzario', {
        'valore' : $input.val()
    });

}

/*********************************************************************************/
$(function(){

        $('#impostaSettore').change(function(){
            var newVal = $(this).val();
            $('#selectPertinenzaNewRow').children('.tmpOption').remove();

            verificaSettorePresente(newVal, 'tmpOption');
        });


        $('#filtraSettori').change(function(){

            filtraTbody( $('#tabellaContainer'), $(this).val());
        });

        $('#filtraSettori').keydown(function(){


            $(this).trigger('change');

        });

        $('#filtraLavorazioni').change(function(){

            filtraRighe( $('#tabellaContainer'), $(this).val());
        });

        $('#filtraLavorazioni').keydown(function(){


            $(this).trigger('change');

        });

        $('#ricarico').change(function(){

            modificaRicaricoAziendale($(this));
        });

});

/**************************************************************************************/

