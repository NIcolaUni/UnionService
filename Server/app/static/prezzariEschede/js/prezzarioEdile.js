/*********************************************************************************************/
var filterZoneOpenWidthPerc = 60;

var arrayAssistenze = [ ['No assistenza',  [] ] ]; // e' un array di array che contiene tutte le assistenze salvate nel db; in particolare ha la forma:
                                                   // [ ['nome_assistenza', [ [tipologia, settore , 'costo', 'tipoCosto' ],...] ], ... ] dove l'ultimo array elemento
                                                   // è l'insieme delle lavorazioni che hanno quel tipo di assistenza

var rowNumber = 0;
var insertRowPhase = false; // evita che nella fase di inserimento di una lavorazione vengango triggerate
                            // certe funzioni
/*******************************************************************/
/* funzione utile a scopo di debugging */

var stampaArrayAssistenze = function(){

    $.each( arrayAssistenze, function(index, el){
        console.log((index+1)+'- assistenza: '+el[0]+'\n');

        $.each(el[1], function(index2, el2){
            console.log((index2+1)+'- Lavorazione: '+el2[0]+' - ' + el2[1] + ' - ' + el2[2] +' - '+ el2[3] + '\n');
        });

        console.log('\n');
    });

}

/*******************************************************************/
var riposizionaTabelle = function(){

    if($('.filterZoneScheda').hasClass('close')){
        $('#sezioneHeader').css('top', '11%' )
    }
    else if($('.filterZoneScheda').hasClass('open')){
        $('#sezioneHeader').css('top', 'unset' )

    }
    allineaVerticalmenteHeader($('#headerTableContainer_1'))

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



    $('#tabellaContainer1 td.pertinenza').each(function(){

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

        $('#tabellaContainer1 tbody').each(function(){
           eliminaSettore($(this));
        });

        $('#tabellaContainer2 tbody').each(function(){
           eliminaSettore($(this));
        });


}


/*************************************************************************************************/

var cancellaRiga = function($row, usernameDip){

    var settore=$row.parent().attr('class');
    var tipo_lav=$row.children('td.tipologia_lavorazione').children('textarea').val();
    var numero_di_riga = $row.attr('class').split('row-')[1];

    var nome_assistenza = $('.row-'+numero_di_riga).children('td.nome_assistenza').children('div').children('select').val();


    rimuoviLavorazioneDaAssistenza(nome_assistenza, tipo_lav, settore );
    modificaSelectAssistenza();
    impostaSelectAssistenzaPerLavorazione();

    socketPrezzario.emit('elimina_lavorazione', {

        'dip': usernameDip,
        'settore': settore,
        'tipologia': tipo_lav

    });

    socketPrezzario.on('conferma_elimina_lav', function(){

        //$row.remove();


        $('.row-'+numero_di_riga).remove();

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

        var numero_di_riga = $row.attr('class').split(' ')[2].split('-')[1];

        if( $row.hasClass('daVerificare') ){
            $row.removeClass('daVerificare');
           // $row.css('background', 'white');
            $('.row-'+numero_di_riga).css('background', 'white');
        }
        else{
            $row.addClass('daVerificare');
           // $row.css('background', 'yellow');
            $('.row-'+numero_di_riga).css('background', 'yellow');
            valore=true;
        }

        socketPrezzario.emit('settaLavorazioneDaVerificare', {
            'settore': settore,
            'tipologia': tipologia,
            'valore': valore
        });

}


/******************************************************************************************/

var equalizzaAltezzaRighe = function(){

    /*trovo la riga più alta*/
    var tallerRow=$('.element_container').first().height();

    $('#tabellaContainer1 .datiScheda').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#tabellaContainer2 .datiScheda').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#tabellaContainer1 .datiScheda').each(function(){
        $(this).height(tallerRow);

    });

    $('#tabellaContainer2 .datiScheda').each(function(){
        $(this).height(tallerRow);
    });


}

/******************************************************************************************/

var equalizzaAltezzaHeader = function(){

    /*trovo la riga più alta*/
    var tallerRow=0;

    $('#headerTableContainer_1 .headerTabella').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#headerTableContainer_2 .headerTabella').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#headerTableContainer_1 .headerTabella').each(function(){
        $(this).height(tallerRow);

    });

    $('#headerTableContainer_2 .headerTabella').each(function(){
        $(this).height(tallerRow);
    });
}

/********************************************************************************************/

var allineaVerticalmenteHeader =function($header){

    /*allineo verticalmente le due tabelle: header e tabella dati*/
    var topRelativeOffsetHeaderContainer = $header.parent().position().top;
    var viewContainerTopPosition = topRelativeOffsetHeaderContainer+$header.height()-1;
    $('.viewContainer').css( {top: viewContainerTopPosition+'px'});

}

/********************************************************************************************/

var allineaOrizzontalmenteHeader =function($header, $tabella){

    var leftOffsetTabella = $tabella.offset().left;
    var leftOffesetHeaderContainer = $header.parent().offset().left;

    var numHeader = parseInt($header.attr('id').split('_')[1]);

    if( numHeader == 1 ){
        //$header.width($(window).height()*70/100);
       // $tabella.width($header.width());

        var diffOffsetContainerTabella = leftOffesetHeaderContainer-leftOffsetTabella;

        $header.css('margin-left', '-'+diffOffsetContainerTabella+'px')

    }
    else if( numHeader == 2 ){
        //$header.width($(window).height()*30/100);
        //$tabella.width($header.width());

        var diffOffsetContainerTabella = leftOffsetTabella-leftOffesetHeaderContainer;

        $header.css('left', diffOffsetContainerTabella+'px')


    }


}

/*******************************************************************************************/
/*
Per ogni prezzario o schedario, la dimensione delle celle della tabella e del suo header
vengoro regolati col codice seguente;
*/

var tabellaSize = $(window).height()*65/100;


var regolaDimensioniHeader = function(idHeaderContainer, idTabellaContainer){

    $('.viewContainer').css( {height: tabellaSize+'px'});

    allineaVerticalmenteHeader( $('#'+idHeaderContainer) );
    allineaOrizzontalmenteHeader( $('#'+idHeaderContainer), $('#'+idTabellaContainer) );

    var numHeader = parseInt($('#'+idHeaderContainer).attr('id').split('_')[1]);

    $('#'+idHeaderContainer).width( $('#'+idTabellaContainer).width() );
    //$('#'+idHeaderContainer).width( $('#'+idTabellaContainer).width() );

    //Per ogni cella dell'header mi assicuro che le dimensioni corrispondano con le
    //celle della tabella contenente i dati

    var indexElement =0;
    var primaColSize = '9%;'

    $('#'+idHeaderContainer+' tbody').children('tr').each(function(){

        if( $(this).hasClass('headerDelHeader') ){

            $('this').children('td.primaCol').css('width', primaColSize );
        }
        else{

            $('#'+idTabellaContainer+' .sezioneTabella').children('td.primaCol').css('width', primaColSize );

            $(this).children('th').each(function(){

                if( numHeader == 1 ){
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
                else{

                    if( $(this).hasClass('nome_assistenza') ){
                        $(this).css('width', '75%')

                    }
                    else if( $(this).hasClass('prezzo_assistenza') ){
                        $(this).css('width', '25%')

                    }

                }

            });

            $('#'+idTabellaContainer+' .datiScheda').children('td').each(function(){

                if( numHeader == 1 ){
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
                     else{


                        if( $(this).hasClass('nome_assistenza') ){
                            $(this).css('width', '75%')

                        }
                        else if( $(this).hasClass('prezzo_assistenza') ){
                            $(this).css('width', '25%')

                        }

                     }
                }

            });
        }
    });

    equalizzaAltezzaRighe();

}

/**************************************************************************************/

var impostaSelectAssistenzaPerLavorazione = function(){


    $('select.selectAssistenzaLavorazione').each(function(){

        var toSel = $(this).parent().children('textarea').val();

        toSel = toSel.replace( /\r?\n/gi, '');
        var lastWordIndex =toSel.length-1;

        if( toSel[lastWordIndex] == ' ' ){
            toSel = valore.slice( 0, lastWordIndex );
        }

        if( toSel == '' )
            $(this).val('No assistenza')
        else
            $(this).val(toSel);

    });

}

/***************************************************************************************/

var aggiungiAssistenzaAdArray = function(nome, costo, tipoCosto, tipo_lav, settore){

     if( nome == '' || nome == 'No assistenza'){

        arrayAssistenze[0][1].push([settore, tipo_lav, costo, tipoCosto ])
     }
     else{

        if( tipoCosto  )
            tipoCosto = 'perc';
         else
            tipoCosto = 'euro';

        /* verifico se ho gia registrato l'assitenza in arrayAssistenze;
            se è registrata semplicemente accodo la lavorazione altrimenti creo un nuovo "rigo" */

        var assistenzaPresente = false;

        $.each(arrayAssistenze, function(index, element){
            if( element[0] == nome ){

                assistenzaPresente = true;
                arrayAssistenze[index][1].push([settore, tipo_lav, costo, tipoCosto ]);

            }

        });

        if(!assistenzaPresente)
            arrayAssistenze.push([ nome, [ [settore, tipo_lav,  costo, tipoCosto ] ] ]);

     }


}

/**************************************************************************************/

var rimuoviLavorazioneDaAssistenza = function( nome_assistenza, tipo_lav, settore ){
    /* se l'assistenza rimane senza lavorazioni associate elimina pure quella */

    if( nome_assistenza == '')
    {
        nome_assistenza = 'No assistenza';
    }

    var counterLavFiglie = 0;
    var indexAssistenza = -1;
    var indexLav = -1;

    //recupero gli indici della lavorazione da eliminare
    $.each( arrayAssistenze, function(index, el){
        if( el[0] == nome_assistenza ){
            indexAssistenza = index;

            $.each(el[1], function(index2, el2){
                counterLavFiglie++;
                if( el2[1] == tipo_lav && el2[0] == settore ){

                    indexLav = index2;
                }
            });
        }
    });

    /*tolgo la lavorazione dall'assistenza a cui era associata */
    if( indexAssistenza >= 0 && indexLav >= 0 ){
        arrayAssistenze[indexAssistenza][1].splice(indexLav, 1);
    }

    if( counterLavFiglie - 1 <= 0 && nome_assistenza != 'No assistenza' ){
        arrayAssistenze.splice(indexAssistenza, 1);
    }


}

/**************************************************************************************/

var modificaDatiAssistenzaInDB = function( nome_assistenza, settore, tipo_lav, campoDaModificare, valore ){
    /* il paramentro 'campoDaModificare' è di tipo intero e vale:
    - 0: per modificare il nome dell'assistenza
    - 1: per modificare il costo
    - 2: per modificare il tipoCosto */

    switch( campoDaModificare ){

        case 0:
            campoDaModificare = 'nome';
            break;
        case 1:
            campoDaModificare = 'costo';
            break;
        case 2:
            campoDaModificare ='prezzoPercentuale';
            if(valore == 'perc')
                valore = true;
            else
                valore = false;

            break;
    }


    socketPrezzario.emit('modifica_assistenza',
    {
        'nome_assistenza' : nome_assistenza,
        'settore': settore,
        'tipo_lav': tipo_lav,
        'toMod' : campoDaModificare,
        'value' : valore

    });

}

/**************************************************************************************/

var modificaDatiAssistenzaInArrayAssistenza = function( nome_assistenza, settore, tipo_lav, campoDaModificare, valore ){

    /* il paramentro 'campoDaModificare' e di tipo intero e vale:
    - 0: per modificare il nome dell'assistenza
    - 1: per modificare il costo
    - 2: per modificare il tipoCosto */

    if( campoDaModificare == 0   ){
        if( valore != nome_assistenza ){
            var costo, tipoCosto, old_assistenza_associata;

            /*l'elimino la vecchia relazione registrata tra assistenza e lavorazione
               salvandomi costo e tipoCosto */

            $.each( arrayAssistenze, function(index, el){

                    $.each(el[1], function(index2, el2){

                        if( el2[1] == tipo_lav && el2[0] == settore ){

                            costo = el2[2];
                            tipoCosto = el2[3];
                            old_assistenza_associata = el[0];

                        }
                    });
            });

            rimuoviLavorazioneDaAssistenza(old_assistenza_associata, tipo_lav, settore);

            if( tipoCosto == 'perc' )
                tipoCosto = true;
            else
                tipoCosto = false;

            /* creo una nuova riga */
            aggiungiAssistenzaAdArray( valore, costo, tipoCosto, tipo_lav, settore );
        }

    }
    else{

        var index1_toMod, index2_toMod;

        $.each( arrayAssistenze, function(index, el){
            if( el[0] == nome_assistenza ){
                $.each(el[1], function(index2, el2){
                    if( el2[1] == tipo_lav && el2[0] == settore ){
                        index1_toMod = index;
                        index2_toMod = index2;

                    }
                });
            }
        });



        if( campoDaModificare == 1 ){
            /*modifico il costo*/
            arrayAssistenze[index1_toMod][1][index2_toMod][2] = valore;

        }
        else if( campoDaModificare == 2 ){
            /*modifico il tipoCosto*/
            arrayAssistenze[index1_toMod][1][index2_toMod][3] = valore;
        }
    }
}



/**************************************************************************************/

var modificaAssistenza = function($this, mod){

    if( !insertRowPhase ){

        /* mod == 0 modifica il nome dell'assistenza, mod == 1 modifica il costo,
            mod == 2 modifica il tipoCosto */

        var numOfRow = $this.parent().parent().parent().attr('class').split(' ')[2];

        var tipo_lav = $('.'+numOfRow).children('td.tipologia_lavorazione').children('textarea').val();

        var settore = $('.'+numOfRow).first().parent().attr('class');

        var nome_assistenza, valore;

        if( mod == 0 ){
            nome_assistenza = $this.parent().children('select').val();
            valore = $this.val().replace( /\r?\n/gi, '');
            var lastWordIndex =valore.length-1;

            if( valore[lastWordIndex] == ' ' ){
                valore = valore.slice( 0, lastWordIndex );
            }
        }
        else{
            nome_assistenza = $this.parent().parent().parent().children('td.nome_assistenza').children('div').children('select').val();
            valore = $this.val();
        }

        modificaDatiAssistenzaInArrayAssistenza( nome_assistenza, settore, tipo_lav, mod, valore );

        if( nome_assistenza == 'No assistenza')
            nome_assistenza ='';

        modificaDatiAssistenzaInDB( nome_assistenza, settore, tipo_lav, mod, valore );

        modificaSelectAssistenza();
        impostaSelectAssistenzaPerLavorazione();

    }
}

/**************************************************************************************/

var modificaNomeAssistenzaGenerale = function($this){


    var nome_assistenza = $('#selectAssistenza').val();

    if( nome_assistenza != 'No assistenza' ){
        swal.withFormAsync({
            title: 'Modifica nome assistenza "'+nome_assistenza+'"',
            showCancelButton: true,
            confirmButtonColor: '#DD6B55',
            confirmButtonText: 'Ok',
            cancelButtonText: 'annulla',
            closeOnConfirm: true,
            formFields: [

                { id: 'nome', label: 'Nuovo nome', name: 'iva', type: 'text', placeholder: 'nome assistenza', value: nome_assistenza },

            ]
        }).then(function (context) {
            if(context._isConfirm){

                /*applico localmente la modifica*/
                var savedIndex;
                $.each( arrayAssistenze, function(index, el){
                    if( el[0] == nome_assistenza )
                        savedIndex = index;
                });

                arrayAssistenze[savedIndex][0] = context.swalForm['nome'];
                $('td.nome_assistenza').children('div.edit_nome_assistenza').children('textarea').each(function(){
                    if( $(this).val() == nome_assistenza )
                        $(this).val(context.swalForm['nome']);
                });

                modificaSelectAssistenza();
                impostaSelectAssistenzaPerLavorazione();

                socketPrezzario.emit('modifica_nome_assistenza_generale', {
                    'old_nome': nome_assistenza,
                    'new_nome':  context.swalForm['nome']
                })

            }
        });
    }
}

/**************************************************************************************/

var eliminaAssistenza = function($this){
    var nome_assistenza = $('#selectAssistenza').val();

    if( nome_assistenza != 'No assistenza' ){
        swal({
              title: 'Eliminazione assistenza: "'+ nome_assistenza+'"',
              text: "sicuro di voler procedere?",
              type: 'info',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: "conferma",
              cancelButtonText: "annulla",
        }, function(isConfirm) {

            if( isConfirm ){

                /*applico localmente la modifica*/
                var savedIndex;
                $.each( arrayAssistenze, function(index, el){
                    if( el[0] == nome_assistenza )
                        savedIndex = index;
                });

                $.each( arrayAssistenze[savedIndex][1],function(index, el){
                    arrayAssistenze[0][1].push(el);
                });

                arrayAssistenze.splice(savedIndex, 1);
                $('td.nome_assistenza').children('div.edit_nome_assistenza').children('textarea').each(function(){
                    if( $(this).val() == nome_assistenza )
                        $(this).val('');
                });

                modificaSelectAssistenza();
                impostaSelectAssistenzaPerLavorazione();


                socketPrezzario.emit('elimina_assistenza',
                    {
                        'nome': nome_assistenza
                    }
                );
            }
        });
    }
}

/**************************************************************************************/

/*popola i vari tag select riguardanti i nomi di assistenza in apertura pagina e li aggiorna
 se viene creata/modificata una nuova assistenza */


var modificaSelectAssistenza = function(){

   $('#selectAssistenza option').remove();

   $('.edit_nome_assistenza select').children('option').remove();


   $.each(arrayAssistenze, function(index, el){
        $('#selectAssistenza ').append('<option class="indexArray-'+index+'">'+el[0]+'</option');
        $('.edit_nome_assistenza select').append('<option class="indexArray-'+index+'">'+el[0]+'</option');
   });


}


/*************************************************************************************/

/*al cambiare del valore del select assistenza di una lavorazione copia il nuovo valore
    nella relativa nell'apposita textarea e aggiorna arrayAssistenze */

var copiaValoreSelectAssistenza = function($this){


    var costo, tipoCosto, indexNewAssistenza;

    /*elimino la vecchia relazione registrata tra assistenza e lavorazione
       salvandomi i dati di quest'ultima e l'indice dell'assistenza selezionata*/
    var numOfRow = $this.parent().parent().parent().attr('class').split(' ')[2];
    var tipo_lav = $('tr.datiScheda.'+numOfRow).children('td.tipologia_lavorazione').children('textarea').val();

    var settore = $this.parent().parent().parent().parent().attr('class');
    var old_assistenza_associata =  $this.parent().children('textarea').val().replace(/\n/g, "");

    $.each( arrayAssistenze, function(index, el){

            $.each(el[1], function(index2, el2){
                if( el2[1] == tipo_lav && el2[0] == settore ){
                    costo = el2[2];
                    tipoCosto = el2[3];

                }
            });
    });

    rimuoviLavorazioneDaAssistenza( old_assistenza_associata, tipo_lav, settore);

    $.each( arrayAssistenze, function(index, el){
            if( el[0] == $this.val() ){
                indexNewAssistenza = index;
            }

    });


    /* creo una nuova associazione assistenza-lavorazione */
    arrayAssistenze[indexNewAssistenza][1].push([settore, tipo_lav, costo, tipoCosto ])


    /*modifico la textarea relativa al select e invio le modifiche al server*/
    if( $this.val() == 'No assistenza'){
        $this.parent().children('textarea').val('');
        modificaDatiAssistenzaInDB( old_assistenza_associata, settore, tipo_lav, 0, '' );
    }
    else{
        $this.parent().children('textarea').val($this.val());
        modificaDatiAssistenzaInDB( old_assistenza_associata, settore, tipo_lav, 0, $this.val() );
    }

    modificaSelectAssistenza();
    impostaSelectAssistenzaPerLavorazione();

}
/**************************************************************************************/

var selectAssistenzaNewRow = function($this){

    var newVal = $this.val();

    $('#newNomeAssistenza').val(newVal);
}

/**************************************************************************************/

var aggiungiRigaAssistenza = function($table2, settore){

    insertRowPhase = true;
    var nome_assistenza = $('#newNomeAssistenza').val().replace(/\n/g, '');
    var costo, tipoCosto;
    var lavorazione = $('tr.row-'+rowNumber).children('td.tipologia_lavorazione').children('textarea').val();
    var settore = $('tr.row-'+rowNumber).parent().attr('class');

    var $datiAssistenza;
    var $tbodyToExpand=null;

    $table2.children('tbody').each(function(){
        if( $(this).attr('class') == settore ){
            $tbodyToExpand=$(this);
        }
    });

    if( nome_assistenza == '' ){
        //se la lavorazione non ha assitenza aggiungo una riga vuota

        $datiAssistenza=$('<tr class="datiScheda dimensionaTabella row-'+rowNumber+'"> \
                            <td class="nome_assistenza" style="width:75%"> \
                                <div class="edit_nome_assistenza"> \
                                    <select class="selectAssistenzaLavorazione" onchange="copiaValoreSelectAssistenza($(this))"> \
                                        <option>opt1</option> \
                                        <option>opt2</option> \
                                    </select> \
                                    <textarea oninput="modificaAssistenza($(this), 0)" placeholder="nome assistenza..."></textarea> \
                                </div> \
                            </td> \
                            <td class="costo_assistenza" style="width:25%"> \
                                <div class="input_costo_assistenza"> \
                                    <input type="number" value="0" oninput="modificaAssistenza($(this), 1)" placeholder="costo..."> \
                                    <input onchange="modificaAssistenza($(this), 2)" type="radio" class="radioBtn perc" name="typeCosto'+rowNumber+'" value="perc">%</input> \
                                    <input onchange="modificaAssistenza($(this), 2)" type="radio" class="radioBtn euro" name="typeCosto'+rowNumber+'" value="euro">&euro;</input>  \
                                </div> \
                            </td> \
                        </tr>').appendTo($tbodyToExpand);

    }
    else{

        costo = $('#costoAssistenzaContainer input[type="number"]').val();


        $datiAssistenza=$('<tr class="datiScheda dimensionaTabella row-'+rowNumber+'"> \
                            <td class="nome_assistenza" style="width:75%"> \
                                <div class="edit_nome_assistenza"> \
                                    <select class="selectAssistenzaLavorazione" onchange="copiaValoreSelectAssistenza($(this))"> \
                                        <option>opt1</option> \
                                        <option>opt2</option> \
                                    </select> \
                                    <textarea oninput="modificaAssistenza($(this), 0)" placeholder="nome assistenza..." value="'+nome_assistenza+'">'+nome_assistenza+'</textarea> \
                                </div> \
                            </td> \
                            <td class="costo_assistenza" style="width:25%"> \
                                <div class="input_costo_assistenza"> \
                                    <input oninput="modificaAssistenza($(this), 1)" type="number" value="'+costo+'" placeholder="costo..."> \
                                    <input onchange="modificaAssistenza($(this), 2)" type="radio" class="radioBtn perc" name="typeCosto'+rowNumber+'" value="perc">%</input> \
                                    <input onchange="modificaAssistenza($(this), 2)" type="radio" class="radioBtn euro" name="typeCosto'+rowNumber+'" value="euro">&euro;</input>  \
                                </div> \
                            </td> \
                        </tr>').appendTo($tbodyToExpand);



        $datiAssistenza.children('td.nome_assistenza').children('div.edit_nome_assistenza').children('select').val($('#newNomeAssistenza').val());

        if( $('#costoAssistenzaContainer input.radioBtn.perc').is(':checked') ){

            tipoCosto = true;
            $datiAssistenza.children('td.costo_assistenza').children('div.input_costo_assistenza').children('input.perc').trigger('click');
        }
        else{

            tipoCosto = false;
            $datiAssistenza.children('td.costo_assistenza').children('div.input_costo_assistenza').children('input.euro').trigger('click');

        }
    }

    aggiungiAssistenzaAdArray( nome_assistenza, costo, tipoCosto, lavorazione, settore);
    modificaSelectAssistenza();
    impostaSelectAssistenzaPerLavorazione();
    insertRowPhase = false;

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


    var $table1=$('#tabellaContainer1').children('table');
    var $table2=$('#tabellaContainer2').children('table');

    if( prezzoMax == 0 ){
        prezzoMax = parseInt($fornitura.val())+parseInt($posa.val());

    }

    var tipoEsistente=false;

    $table1.children('tbody').each(function(){
        if( $(this).attr('class') == $settore.val() ){
            tipoEsistente = true;
        }
    });

    if( !tipoEsistente ){


        $table1.append(
            '<tbody class="'+$settore.val()+'"> \
                <tr class="sezioneTabella dimensionaTabella""> \
                    <th class="primaCol"></th> \
                    <th class="secondaCol" colspan="11">Settore di lavorazione: '+$settore.val()+'</th> \
                </tr> \
            <tbody>'
        );

        $table2.append(
            '<tbody class="'+$settore.val()+'"> \
                <tr class="sezioneTabella dimensionaTabella""> \
                    <th class="secondaCol" colspan="2"></th> \
                </tr> \
            <tbody>'
        );


    }

    var $tbodyToExpand=null;

    $table1.children('tbody').each(function(){
        if( $(this).attr('class') == $settore.val() ){
            $tbodyToExpand=$(this);
        }
    });

    var tipologia = $tipologia.val().replace(/\n/g, "");
    var note = $note.val().replace(/\n/g, "");


    var datiSchedaNewRow=$(
                    '<tr class="datiScheda dimensionaTabella row-'+rowNumber+'"> \
                        <td class="primaCol"> \
                             <a class="fa fa-warning primaColIcon segnalaRow"></a><a class="fa fa-trash primaColIcon delRow"></a> \
                        </td> \
                         <td class="tipologia" style="display:none"> \
                            <input class="inputScheda" value="'+tipologia+'"> \
                        </td> \
                        <td class="tipologia_lavorazione"> \
                            <textarea class="inputScheda cellaTextarea" placeholder="tipologia lavorazione..." >'+tipologia+'</textarea>\
                        </td> \
                        <td class="pertinenza hiddenInput"> \
                            <select></select> \
                        </td> \
                        <td class="unitaMisura numCellBig">\
                            <select> \
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
                        <td class="note"> \
                           <textarea class="cellaTextarea">'+note+'</textarea> \
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

        if( attributoToEdit == 'note' || attributoToEdit == 'tipologia_lavorazione' ){
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

    $('#tabellaContainer1 input').unbind('change').change(function(){

        changeValueLavorazione($(this));
    });

    $('#tabellaContainer1 textarea').unbind('change').change(function(){

        changeValueLavorazione($(this));
    });

    $('#tabellaContainer1 select').unbind('change').change(function(){
        changeValueLavorazione($(this));

    });

    aggiungiRigaAssistenza($table2, $settore.val());

    if( daVerificare )
        segnalaRiga(datiSchedaNewRow)

    rowNumber++ ;

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

var checkboxBehavor = function($bottone){

    if( $bottone.hasClass('checked') ){
        $bottone.css('visibility', 'hidden');
        $bottone.removeClass('checked');

    }
    else{
        $bottone.addClass('checked');
        $bottone.css('visibility', 'visible');

    }
}

/*********************************************************************************/

var implementaBottoneMostraAssistenza = function($bottone){

    var offsetFromTop = $('#tabellaContainerNewRow2').height();

    if( $bottone.hasClass('checked') ){
        /*nascondo la parte di tabella nascosta */
        $('#tabellaContainerNewRow2').animate({'margin-top': '+='+offsetFromTop+'px'});

    }
    else{

        /*mostro la parte di tabella nascosta */
        $('#tabellaContainerNewRow2').animate({'margin-top': '-='+offsetFromTop+'px'});

    }
}
/*********************************************************************************/

var implementaBottoneNuovaAssistenza = function($bottone){

    if( $bottone.hasClass('checked') ){

        $('#newNomeAssistenza').parent().show();
        $('#newNomeAssistenza').val('');
        $('#selectAssistenzaContainer').hide();
        $('#costoAssistenzaContainer input[type="number"]').val(0);
       // $('#labelCostoAssistenzaContainer').hide();

    }
    else{
        $('#newNomeAssistenza').parent().hide();
       // $('#costoAssistenzaContainer').hide();
        $('#selectAssistenzaContainer').show();

        var indexAssistenza = parseInt($('#selectAssistenza option:selected').attr('class').split('-')[1]);
        $('#newNomeAssistenza').val($('#selectAssistenza').val());

        $('#costoAssistenzaContainer input[type="number"]').val(arrayAssistenze[indexAssistenza][1][2]);

        if( arrayAssistenze[indexAssistenza][1][3] == 'perc' )
            $('#costoAssistenzaContainer input.radioBtn.perc').trigger('click');
        else
            $('#costoAssistenzaContainer input.radioBtn.euro').trigger('click');



       // $('#labelCostoAssistenzaContainer').show();

    }
}

/*********************************************************************************/
$(function(){

        $('#impostaSettore').change(function(){
            var newVal = $(this).val();
            $('#selectPertinenzaNewRow').children('.tmpOption').remove();

            verificaSettorePresente(newVal, 'tmpOption');
        });


        $('#filtraSettori').change(function(){

            filtraTbody( $('#tabellaContainer1'), $(this).val());
        });

        $('#filtraSettori').keydown(function(){


            $(this).trigger('change');

        });

        $('#filtraLavorazioni').change(function(){

            filtraRighe( $('#tabellaContainer1'), $(this).val());
        });

        $('#filtraLavorazioni').keydown(function(){


            $(this).trigger('change');

        });

        $('#ricarico').change(function(){

            modificaRicaricoAziendale($(this));
        });


        $('#buttonAssistenza').click(function(){

            checkboxBehavor($('#buttonAssistenza a'));
            implementaBottoneMostraAssistenza($('#buttonAssistenza a'));
        });

        $('#aggiungiAssistenza label').click(function(){

            checkboxBehavor($('#buttonAssistenza a'));
            implementaBottoneMostraAssistenza($('#buttonAssistenza a'));
        });

        $('#delNewRow').click(function(){
            if( $('#buttonAssistenza a').hasClass('checked') ){
                checkboxBehavor($('#buttonAssistenza a'));
                implementaBottoneMostraAssistenza($('#buttonAssistenza a'));
            }
        });


        /* Inizialmente nascondo la parte dell'"aggiungiRiga" che riguarda l'assistenza */
        var offsetFromTop = $('#tabellaContainerNewRow2').height();
        $('#tabellaContainerNewRow2').animate({'margin-top': '-='+offsetFromTop+'px'});


        $('#buttonNuovaAssistenza').click(function(){

            checkboxBehavor($('#buttonNuovaAssistenza a'));
            implementaBottoneNuovaAssistenza($('#buttonNuovaAssistenza a'));

        });

        $('#aggiungiNuovaAssistenza label').click(function(){

            checkboxBehavor($('#buttonNuovaAssistenza a'));
            implementaBottoneNuovaAssistenza($('#buttonNuovaAssistenza a'));

        });

       // $('textarea#newNomeAssistenza').on

        setTimeout(function(){
            equalizzaAltezzaHeader();
            window.addEventListener('resize', equalizzaAltezzaHeader());
        }, 100);
});

/**************************************************************************************/

