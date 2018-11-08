var filterZoneOpenWidthPerc = 60;

/*******************************************************************/
var riposizionaTabelle = function(){

}

/*******************************************************************************************/
/*
Per ogni prezzario o schedario, la dimensione delle celle della tabella e del suo header
vengoro regolati col codice seguente;
*/

var tabellaSize = $(window).height()*65/100;

var regolaDimensioniHeader = function(idHeaderContainer, idTabellaContainer){

    $('.viewContainer').css( {height: tabellaSize+'px'});

    $('#'+idHeaderContainer).width( $('#'+idTabellaContainer).width());

    //Per ogni cella dell'header mi assicuro che le dimensioni corrispondano con le
    //celle della tabella contenente i dati

    var indexElement =0;
    var primaColSize = '10%;'

    $('#'+idHeaderContainer+' tbody').children('tr').each(function(){

        if( $(this).hasClass('headerDelHeader') ){
        //    alert('qua: '+$(this).attr('class'))

            $('this').children('td.primaCol').css('width', primaColSize );
        }
        else{

            $('#'+idTabellaContainer+' .sezioneTabella').children('td.primaCol').css('width', primaColSize );

            $(this).children('th').each(function(){

                if( $(this).hasClass('primaCol') ){
                    $(this).css('width', primaColSize)
                }
                else if( $(this).hasClass('normal_string')  ){
                    $(this).css('width', '16%')

                }

                else if( $(this).hasClass('note') ){
                    $(this).css('width', '20%')

                }
                else if( $(this).hasClass('numCellBig') ){
                    $(this).css('width', '6%')

                }

            });

            $('#'+idTabellaContainer+' .datiScheda').children('td').each(function(){
                //L'if qua sotto esclude le celle che sono usate per memorizzare la chiave della riga
                 if(!$(this).hasClass('nominativo_saved')){

                    if( $(this).hasClass('primaCol') ){
                        $(this).css('width', primaColSize)
                    }
                    else if( $(this).hasClass('normal_string')  ){
                        $(this).css('width', '16%')

                    }

                    else if( $(this).hasClass('note') ){
                        $(this).css('width', '20%')

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

var hiddenInputAction = function($this){

    $('.inModifica').each(function(){
        $(this).removeClass('inModifica');
        $(this).children('label').show();
        $(this).children('input').hide();
        $(this).children('textarea').hide();


    });


    $this.addClass('inModifica');
    $this.children('label').hide();
    $this.children('input').show();
    $this.children('textarea').show();

}

/**************************************************************************************/

var verificaImpiegoVuoto = function(){

     /*se una sezione rimane senza artigiano elimino l'impiego*/
    var eliminaImpiego= function($this){
       var counter = 0;

       $this.children('tr').each(function(){
            counter++;

       });


       if( counter == 1 ){

        $this.remove();
       }

    }

    $('#tabellaContainer tbody').each(function(){
       eliminaImpiego($(this));
    });


}

/**************************************************************************************/

var cancellaRiga = function($row, usernameDip){

    var impiego=$row.parent().attr('class');
    var nominativo=$row.children('td.nominativo_saved').children('input').val();

    socketArtigiani.emit('elimina_artigiano', {

        'dip': usernameDip,
        'impiego': impiego,
        'nominativo': nominativo

    });

    socketArtigiani.on('conferma_elimina_artigiano', function(){

        $row.remove();

        verificaImpiegoVuoto();

    });

}

/**************************************************************************************/

var pulisciHeaderNewRow = function(){

    $('#headerNewRow input').each(function(){
        if($(this).hasClass('inputNum'))
            $(this).val(0);
        else
        {
            $(this).val('');

        }
    });

    $('#headerNewRow textarea').each(function(){

        $(this).val('');

    });

}


/**************************************************************************************/
var artigianoInListaArtigiani = function(artigiano){

    var toAdd = true;

    $('#listArtigiani').children('option').each(function(){
        if( $(this).val() == artigiano ){
            toAdd = false;
        }
    });

    if( toAdd ){
        $('#listArtigiani').append('<option>'+artigiano+'</option>');
    }
}

/**************************************************************************************/

var aggiungiRiga = function(usernameDip){

    var $tbodyNewRow1=$('#tabellaContainerNewRow1').children('table').children('tbody');
    var $datiScheda1=$tbodyNewRow1.children('.datiScheda');
    var $sezioneTabella1=$tbodyNewRow1.children('.sezioneTabella');

    var $impiego = $sezioneTabella1.children('th.primaCol').next('th').children('input');
    var $nominativo = $datiScheda1.children('td.nominativo').children('input');
    var $valutazione = $datiScheda1.children('td.valutazione').children('input');
    var $contatti1 = $datiScheda1.children('td.contatti1').children('input');
    var $contatti2 = $datiScheda1.children('td.contatti2').children('input');
    var $email = $datiScheda1.children('td.email').children('input');
    var $note = $datiScheda1.children('td.note').children('textarea');


     var $table=$('#tabellaContainer').children('table');

    var impiegoEsistente=false;

    $table.children('tbody').each(function(){
        if( $(this).attr('class') == $impiego.val() ){
            impiegoEsistente = true;
        }
    });

    if( !impiegoEsistente ){
        $table.append(
            '<tbody class="'+$impiego.val()+'"> \
                <tr class="sezioneTabella dimensionaTabella""> \
                    <th class="primaCol"></th> \
                    <th class="secondaCol" colspan="6">Impiego: '+$impiego.val()+'</th> \
                </tr> \
            <tbody>'
        );

    }
    var $tbodyToExpand=null;

    $table.children('tbody').each(function(){
        if( $(this).attr('class') == $impiego.val() ){
            $tbodyToExpand=$(this);
        }
    });

    artigianoInListaArtigiani($nominativo.val())

    var datiSchedaNewRow=$(
                '<tr class="datiScheda dimensionaTabella"> \
                    <td class="primaCol"> \
                        <a class="fa fa-trash primaColIcon delRow"></a> \
                        <div class="divColorChoose"> \
                            <input type="radio" name="colorChoose" class="yellow" value="yellow"> \
                            <input type="radio" name="colorChoose" class="blue" value="blue"> \
                            <input type="radio" name="colorChoose" class="green" value="green"> \
                            <input type="radio" name="colorChoose" class="gray" value="gray"> \
                            <input type="radio" name="colorChoose" class="white" value="white"> \
                            <span class="spanColorChoose yellow"> </span> \
                            <span class="spanColorChoose blue"> </span> \
                            <span class="spanColorChoose green"> </span> \
                            <span class="spanColorChoose gray"> </span> \
                            <span class="spanColorChoose white"> </span> \
                        </div> \
                    </td> \
                    <td class="nominativo_saved" style="display:none"> \
                        <input  class="inputScheda" value="'+$nominativo.val()+'" placeholder="nome artigiano..." > \
                    </td> \
                    <td class="nominativo hiddenInput normal_string"> \
                        <label class="cellaDato">'+$nominativo.val()+'</label> \
                        <input style="display:none" class="inputScheda" value="'+$nominativo.val()+'" placeholder="nome artigiano..." > \
                    </td> \
                    <td class="valutazione hiddenInput numCellBig"> \
                        <label class="cellaDato">'+$valutazione.val()+'</label> \
                        <input style="display:none" type="number" class="inputScheda inputNum" value="'+$valutazione.val()+'" placeholder="valutazione artigiano..." > \
                    </td> \
                    <td class="contatti1 hiddenInput normal_string"> \
                        <label class="cellaDato">'+$contatti1.val()+'</label> \
                        <input style="display:none" type="tel" class="inputScheda" value="'+$contatti1.val()+'" placeholder="contatto 1..." > \
                    </td> \
                    <td class="contatti2 hiddenInput  normal_string"> \
                        <label class="cellaDato">'+$contatti2.val()+'</label> \
                        <input style="display:none" type="tel" class="inputScheda" value="'+$contatti2.val()+'" placeholder="contatto 2..." > \
                    </td> \
                    <td class="email hiddenInput  normal_string"> \
                        <label class="cellaDato">'+$email.val()+'</label> \
                        <input style="display:none" type="email" class="inputScheda" value="'+$email.val()+'" placeholder="email artigiano..." > \
                    </td> \
                    <td class="note hiddenInput"> \
                        <label class="cellaDato">'+$note.val()+'</label> \
                        <input style="display:none" class="inputScheda" value="'+$note.val()+'" placeholder="note artigiano..." > \
                    </td> \
                </tr>').appendTo($tbodyToExpand);


    $('td.hiddenInput').click( function(){
        hiddenInputAction($(this));

    });


    datiSchedaNewRow.children('td.primaCol').children('div').children('input').change(function(){



        var color = $(this).attr('class');

        datiSchedaNewRow.css('background', color);

        if( color != 'yellow' && color != 'white' ){
            datiSchedaNewRow.css('color', 'white');
        }
        else
            datiSchedaNewRow.css('color', '#797877');


        var $riga=$(this).parent().parent().parent();
        var impiego= $riga.parent().attr('class');
        var nominativo = $riga.children('td.nominativo_saved').children('input').val();

        socketArtigiani.emit('modifica_colore_artigiano', {

            'impiego': impiego,
            'nominativo': nominativo,
            'colore': color

        });

    });

    datiSchedaNewRow.children('td.primaCol').children('div').children('span.spanColorChoose').click(function(){

        var color = $(this).attr('class').split(' ')[1];
        $(this).parent().children('input.'+color).trigger('click');
        $(this).parent().children('input.'+color).trigger('change');

    });


    datiSchedaNewRow.children('td.primaCol').children('a.delRow').click(function(){

        cancellaRiga(datiSchedaNewRow, usernameDip);
    });

    $('input').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    $('textarea').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    var changeValueArtigiano = function($this){

        var $container=$this.parent();
        var $row = $container.parent();
        var impiego = $row.parent().attr('class');
        var nominativo=$row.children('td.nominativo_saved').children('input').val();

        var attributoToEdit=$container.attr('class').split(' ')[0];
        var valore = $this.val()

        if( attributoToEdit == 'note' ){
            valore= $this.val().replace( /\r?\n/gi, '');

        }

        socketArtigiani.emit('modifica_artigiano',
            {
                'dip' : usernameDip,
                'impiego' : impiego,
                'nominativo' : nominativo,
                'toEdit' : attributoToEdit,
                'valore' : valore
            }
        );

        socketArtigiani.on('conferma_modifica_artigiano', function(){

            $('.inModifica').each(function(){

                $(this).children('label').show();
                $(this).children('input').hide();
                $(this).children('textarea').hide();

                $(this).removeClass('inModifica');
            });


            if( $container.hasClass('numCell') ){
                if($container.hasClass('fornitura') || $container.hasClass('posa') ){
                    calcolaCostoFornituraPosa(datiSchedaNewRow);
                }
                $container.children('label.cellaDato').html('&euro; '+valore);
            }
            else{
                $container.children('label.cellaDato').html(valore);
            }


            if( attributoToEdit == 'nominativo' ){
                $row.children('td.nominativo_saved').children('input').val(valore);
            }

        });


    }

    $('#tabellaContainer input').each(function(){

        if( $(this).attr('type') != 'radio' ){
            $(this).unbind('change').change(function(){

                changeValueArtigiano($(this));
            });
        }


    });

    $('#tabellaContainer textarea').unbind('change').change(function(){

        changeValueArtigiano($(this));
    });

    return datiSchedaNewRow;

} //FINE AGGIUNGI RIGA



/**************************************************************************************/

var filtraTbody = function($tabella, classe){

    if( classe != '' ){
        $tabella.children('table').children('tbody').each(function(){
            var tbodyClass = $(this).attr('class');

            if( tbodyClass !== undefined ){

                if( !tbodyClass.startsWith(classe) ){
                    $(this).hide();
                }
                else if( tbodyClass.startsWith(classe) ){
                    $(this).show();
                }

            }
        });
    }
    else{
        $tabella.children('table').children('tbody').each(function(){
            $(this).show();
        });

    }
}

/**************************************************************************************/

var filtraRighe = function($tabella, nominativo){

    if( nominativo != '' ){

        $tabella.children('table').children('tbody').each(function(){

            var tbodyClass = $(this).attr('class');

            if( tbodyClass !== undefined ){
                var hideTbody = false;
                var countRow = 0;
                var countHiddenRow = 0;


                $(this).children('tr.datiScheda').each( function(){
                    var trNominativo = $(this).children('td.nominativo_saved').children('input').val();

                    countRow++;

                    if( trNominativo.startsWith(nominativo) ){
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


/**************************************************************************************/

$(function(){


    $('#filtraImpieghi').change(function(){

        filtraTbody( $('#tabellaContainer'), $(this).val());
    });

    $('#filtraImpieghi').keydown(function(){


        $(this).trigger('change');

    });

    $('#filtraArtigiani').change(function(){

        filtraRighe( $('#tabellaContainer'), $(this).val());
    });

    $('#filtraArtigiani').keydown(function(){


        $(this).trigger('change');

    });
});
