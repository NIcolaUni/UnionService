/************************************************************************************************/
var numeroPreventivo;
var revisionePreventivo;
/* variabile globale usata per tener conto del numero dell'ultima lavorazione aggiunta */
var ordineLavorazioni = 1;

var disabilitaSocketio = false;
var cbxStatus = true;

var lavToCtrl = []; /* array usato in modalità modifica per aggiungere correttamente le lavorazioni;
                            i suoi elementi sono array della forma [ id_lav, settore ] */
var lavToCtrl_changed = false;

var arrayAssistenze = []; //memorizzo le assistenze originali di una lavorazione coi suoi dati;
                          // l'array ha la forma: [ [ id_riga_assistenza, nome_assistenza, costo, tipo_costo ], ... ]

/********************************************************************************************/
/* funzione per il debug */

var stampaLavToCtrl= function(){


    $.each(lavToCtrl, function(index, el){

        alert( 'Riga '+ (index+1) +': ');
        alert( el[0] + ' - ' + el[1]  );


    });

}

/********************************************************************************************/
/* funzione per il debug */

var stampaArrayAssistenza = function(){


    $.each(arrayAssistenze, function(index, el){

        console.log( 'Riga '+ (index+1) +': ');
        console.log( el[0] + ' - ' + el[1] + ' - ' + el[2] + ' - ' + el[3] );


    });

}

/********************************************************************************************/

var espandiTabella = function(){

    if(cbxStatus == true ){

        $('.titleSettoreTd').attr('colspan', 13 );
        $('.thAdded').show();
        $('.tdAdded').show();
        $('#ricarichiSection').show();

        cbxStatus=false;
    }
    else{

        $('.titleSettoreTd').attr('colspan', 10 );
        $('.thAdded').hide();
        $('.tdAdded').hide();
        $('#ricarichiSection').hide();

        cbxStatus=true;

    }
}


/***********************************************************************************************/

var stampaPreventivo = function(usernameDip){

    swal.withFormAsync({
        title: 'Scelte pre-stampa:',
        showCancelButton: true,
        confirmButtonColor: '#DD6B55',
        confirmButtonText: 'Ok',
        cancelButtonText: 'annulla',
        closeOnConfirm: false,
        formFields: [

            { id: 'iva', label: 'Iva (%)', name: 'iva', type: 'number', placeholder: 'intervento commessa', value: '0' },
            { id: 'scontoTipo',
                type: 'select-hidden',
                options: [
                  {value: '1', text: 'non applicare sconto'},
                  {value: '2', text: 'applica sconto netto'},
                  {value: '3', text: 'applica sconto percentuale'},
                  {value: '4', text: 'forza totale'},
                ]},
            { id: 'sumisura', label: 'Preventivo a misura', name: 'sumisura', value: 'sumisura', type: 'checkbox' },
            { id: 'chiudi', label: 'Chiudi preventivo', name: 'chiudi', value: 'chiudi', type: 'checkbox' },

        ]
    }).then(function (context) {
        if(context._isConfirm){

            var sceltaSconto=parseInt(context.swalForm['scontoTipo']);
            var chiudiPrev=false;
            var sumisura=false;
            var iva=parseInt(context.swalForm['iva']);
            if( context.swalForm['chiudi'] == 'chiudi' ){
                chiudiPrev=true;

            }

            if( context.swalForm['sumisura'] == 'sumisura' )
                sumisura=true;


            if( sceltaSconto == 1 ){
                socketPreventivo.emit('stampa_preventivo', {
                                                'dip': usernameDip,
                                                'numero_preventivo': numeroPreventivo,
                                                'revisione': revisionePreventivo,
                                                'iva': iva,
                                                'tipoSconto': sceltaSconto,
                                                'sconto': 0,
                                                'chiudiPreventivo': chiudiPrev,
                                                'sumisura': sumisura });
                sweetAlert.close();
            }
            else{
                var toPrint="";
                var valueSconto = '0'


                if( sceltaSconto == 2 ){
                    toPrint ="Inserire sconto netto da applicare:";
                }
                else if( sceltaSconto == 3 ){
                    toPrint ="Inserire sconto percentuale da applicare:";
                }
                else if( sceltaSconto == 4 ){
                    toPrint = "Forza totale:";
                    valueSconto = $('#divTotale').children('span').text().split(' ')[2];
                }




                swal.withFormAsync({
                    title: toPrint,
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Ok',
                    cancelButtonText: 'annulla',
                    closeOnConfirm: true,
                    formFields: [

                        { id: 'sconto', name: 'sconto', type: 'number', placeholder: 'sconto', value: valueSconto },


                    ]
                }).then(function (context) {
                    if(context._isConfirm){
                         socketPreventivo.emit('stampa_preventivo', {
                                                'dip': usernameDip,
                                                'numero_preventivo': numeroPreventivo,
                                                'revisione': revisionePreventivo,
                                                'iva': iva,
                                                'tipoSconto': sceltaSconto,
                                                'sconto': parseFloat(context.swalForm['sconto']),
                                                'chiudiPreventivo': chiudiPrev,
                                                'sumisura': sumisura });

                    }

                });

            }



        }

    });

}

/***********************************************************************************************/

var aggiungiNote = function($this){

    socketPreventivo.emit('inserisci_note', {   'numero_preventivo': numeroPreventivo,
                                                        'revisione': revisionePreventivo,
                                                        'nota': $this.val() });

}


/*******************************************************************************************/

var resettaLavToCtrl = function(){

        var tmp = []
        $('.trBody').each(function(){


            var settore = $(this).attr('id').split('_trBody-')[0];

            $('.trHead.'+settore ).children('td.titleSettoreTd').each(function(){

                if(!$(this).hasClass('totaleSettore')){
                    settore = $(this).text();
                }
            });


            tmp.push([ $(this).attr('id'), settore ]);



        });

        lavToCtrl = tmp;
        lavToCtrl_changed = true;

}


/************************************************************************************************/

var rienumeraPagina = function( ){

    var counter = 1;
    var oldNum="";


    //rinomino tutti gli id degli elementi per non rischiare di
    //averne due uguali nella rienumerazione.
    $('.trBody').each(function(){

        var classSettore = $(this).attr('id').split('_trBody-')[0];
        oldNum = $(this).attr('id').split('_trBody-')[1]

        $(this).attr('id', classSettore+'_trBody-old'+oldNum);


        $('.'+classSettore+'_trSottolavorazione-'+oldNum).addClass(classSettore+'_trSottolavorazione-old'+oldNum);
        $('.'+classSettore+'_trSottolavorazione-'+oldNum).removeClass(classSettore+'_trSottolavorazione-'+oldNum);

        $(this).next('.trFoot'+oldNum).addClass('trFoot-old'+oldNum);
        $(this).next('.trFoot'+oldNum).removeClass('trFoot'+oldNum);

        /* nel caso vi siano righe aggiunte il next non recupera il "trFoor" specifico;
          con questo comando si previene questa eventualita' */
        $("."+classSettore+"_trFoot").each(function(){
            if($(this).hasClass('trFoot'+oldNum)){
                $(this).addClass('trFoot-old'+oldNum);
                $(this).removeClass('trFoot'+oldNum);

            }
        });

        $(this).children('.firstCol'+oldNum).addClass('firstCol-old'+oldNum);
        $(this).children('.firstCol'+oldNum).removeClass('firstCol'+oldNum);
        $(this).children('.firstCol-old'+oldNum).children('.add-'+oldNum).addClass('add-old'+oldNum);
        $(this).children('.firstCol-old'+oldNum).children('.add-'+oldNum).removeClass('add-'+oldNum);

        /*modifico i pulsanti "aggiungi elemento" degli elementi presenti
            e la memoria apposita*/
        $('.aggiunto-'+oldNum).addClass('aggiunto-old'+oldNum);
        $('.aggiunto-'+oldNum).removeClass('aggiunto-'+oldNum);

        $('#memoriaLavorazioniAggiunte').children('.settoreMemorizzato').each(function(){

            $(this).children('div').each(function(){
                var oldName = $(this).text()
                $(this).text('aggiunto-old-'+oldName.split('-')[1]);

            });

        });


    });

    /* effettuo la stessa operazione di ridenominazione su arrayAssistenze */

    $.each(arrayAssistenze, function(index, el){
        el[0] = el[0].split('_trBody-')[0]+'_trBody-old'+el[0].split('_trBody-')[1];
    });


    /*effettuo l'effettiva rienumerazione*/
    $('.trBody').each(function(){
        var classSettore = $(this).attr('id').split('_trBody-')[0];

        oldNum =  $(this).attr('id').split('-old')[1];

        $('.aggiunto-old'+oldNum).addClass('aggiunto-'+counter);
        $('.aggiunto-old'+oldNum).removeClass('aggiunto-old'+oldNum);

        /*rienumero la memoria lavorazioni*/
        var buttonId = $('.aggiunto-'+counter).attr('id')
        $('#memoriaLavorazioniAggiunte').children('.settoreMemorizzato').each(function(){

            $(this).children('div.'+buttonId).each(function(){
                $(this).text('aggiunto-'+counter);

            });

        });


        $(this).attr('id', classSettore+'_trBody-'+counter);

        $(this).children('.firstCol-old'+oldNum).addClass('firstCol'+counter);
        $(this).children('.firstCol-old'+oldNum).removeClass('firstCol-old'+oldNum);

        $(this).children('.firstCol'+counter).children('label').text(counter);
        $(this).children('.firstCol'+counter).children('.add-old'+oldNum).addClass('add-'+counter);
        $(this).children('.firstCol'+counter).children('.add-old'+oldNum).removeClass('add-old'+oldNum);
        $(this).children('td.tdCostoAssistenza').children('div').children('div').children('input').attr('name', classSettore+'_trBody-'+counter );


        $oldSottolavorazioneRows=$('.'+classSettore+'_trSottolavorazione-old'+oldNum);

        $oldSottolavorazioneRows.children('.inputField').children('.numInput').each(function(){
            $(this).removeClass('inputPrev-'+oldNum);
            // questa operazione e' per mantenere l'ordine originario delle classi, importante per
            // recuperare correttamente tutte le informazioni indispensabili.
            var typeOfDim=$(this).attr('class').split(' ')[1];
            $(this).removeClass(typeOfDim);

            $(this).addClass('inputPrev-'+counter);
            $(this).addClass(typeOfDim);
        });


        $oldSottolavorazioneRows.each(function(){
            $(this).removeClass(classSettore+'_trSottolavorazione-old'+oldNum);
            var oldSottolavorazioneRowClasses=$(this).attr('class');
            $(this).removeClass(oldSottolavorazioneRowClasses);
            $(this).addClass(classSettore+'_trSottolavorazione-'+counter);
            $(this).addClass(oldSottolavorazioneRowClasses);
        });

        $(this).next('.trFoot-old'+oldNum).addClass('trFoot'+counter);
        $(this).next('.trFoot-old'+oldNum).removeClass('trFoot-old'+oldNum);

        /* nel caso vi siano righe aggiunte il next non recupera il "trFoot" specifico;
          con questo comando si previene questa eventualita' */
        $("."+classSettore+"_trFoot").each(function(){
            if($(this).hasClass('trFoot-old'+oldNum)){
                $(this).addClass('trFoot'+counter);
                $(this).removeClass('trFoot-old'+oldNum);

            }
        });

        try{
            var unitaMisura = $('.trFoot'+counter).attr('class').split(' ')[2].split('-')[1];
        }
        catch(err){
            console.log('lavorazione_fantasma')
        }
        //unitaMisura = unitaMisura.split('_')[0]+' '+unitaMisura.split('_')[1];

        /*rienumero gli elementi di arrayAssistenze */

        $.each(arrayAssistenze, function(index, el){
            if( el[0] == classSettore+'_trBody-old'+oldNum ){
                el[0] = classSettore+'_trBody-'+counter;
            }

        });

        if( !disabilitaSocketio ){
            socketPreventivo.emit("modifica_ordine_lavorazione",
                            {
                                "numero_preventivo" : numeroPreventivo,
                                "revisione" : revisionePreventivo,
                                "unitaMisura" : unitaMisura,
                                "ordineVecchio": oldNum,
                                "ordineNuovo" : counter

                            }
                  );
        }
        counter+=1;
    });


    resettaLavToCtrl();
}


/***********************************************************************************************/

var calcolaTotalePreventivo = function(){
    var totale = 0;

    $('.trBody').each(function(){
            var numEl = $(this).attr('id').split('_trBody-')[1];
            totale+=parseFloat($('.trFoot'+numEl).children('.footTot').text().split(' ')[1]);

    });

   /* var totaleUs = 0;

    $('.trBody').each(function(){
            var numEl = $(this).attr('id').split('_trBody-')[1];
            totale+=parseFloat($('.trFoot'+numEl).children('.footTot').text().split(' ')[1]);

    });
*/

    $('#divTotale').html('<span><u>Totale cliente:</u> &euro; ' + Math.round(totale*100)/100 + '</span>' );
}


/***********************************************************************************************/

var calcolaTotaleParzialeSettore = function( classSettore ){
    var totale = 0;

    $("."+classSettore+"_trFoot").each(function(){
        totale += parseFloat($(this).children('.footTot').text().split(' ')[1]);

    });

    totale = Math.round(totale*100)/100;

    $('.trHead.'+classSettore).each(function(){

        $(this).children('.totaleSettore').html('&euro; '+totale );

    });
}

/***********************************************************************************************/

var calcolaTotaleParziale = function(classSettore, numOfEl){

        var total = 0;
        var quantita =0;

        $('.'+classSettore+'_trSottolavorazione-'+numOfEl).each(function(){
            total+=parseFloat($(this).children('.totalSottolavorazione').text().split(' ')[1]);
            quantita+=parseFloat($(this).children('.totDimensioni').text());
        });


        $('.trFoot'+numOfEl).children('.footTot').html("&euro; "+ Math.round(total*100)/100 );
        $('.trFoot'+numOfEl).children('.quantita').html(Math.round(quantita*100)/100);

        calcolaTotaleParzialeSettore( classSettore );
        calcolaTotalePreventivo();
}

/*********************************************************************************************/

var calcolaTotaleRigaSottolavorazione = function(classeElemento, ordineSottolav, prezzoBase){
    /*
        Il paramentro "classeElemento" ha la forma: "<classesettore>_trSottolavorazione-<ordineLavorazione>"
        Il parametro "ordineSottolav" ha la forma: "sottolavNum-<ordineSottolavorazione>"

    */
    var classeElementoSplitted = classeElemento.split('_trSottolavorazione-');
    var idContainerLav = classeElementoSplitted[0]+'_trBody-'+classeElementoSplitted[1];
    var inputAssistenzaContainer = $('#'+idContainerLav).children('td.tdCostoAssistenza').children('div');
    var costoAssistenza = parseFloat(inputAssistenzaContainer.children('input[type="number"]').val());
    var tipoCostoAssistenza = inputAssistenzaContainer.children('div').children('input[type="radio"]:checked').val();

    $('.'+classeElemento+'.'+ordineSottolav).each(function(){


        var totalePrezzo=parseFloat(prezzoBase);

        if( tipoCostoAssistenza == 'perc' ){
           totalePrezzo += ( totalePrezzo*costoAssistenza/100 )
        }
        else {
            totalePrezzo += costoAssistenza;
        }



        var quantita=1;


        $(this).children('td.inputField').each(function(){
           quantita=quantita*parseFloat($(this).children('input').val());

        });

        totalePrezzo=parseFloat(totalePrezzo)*quantita;


        $(this).children('td.totDimensioni').text( Math.round(quantita*100)/100 );
        $(this).children('td.totalSottolavorazione').html( "&euro; " + Math.round(totalePrezzo*100)/100 );

    });

    calcolaTotaleParziale(classeElemento.split('_trSottolavorazione-')[0], classeElemento.split('_trSottolavorazione-')[1]);
}

var calcolaTotaleUs = function( classeElemento, ordineSottolav ){
    /*
        Il paramentro "classeElemento" ha la forma: "<classesettore>_trSottolavorazione-<ordineLavorazione>"
        Il parametro "ordineSottolav" ha la forma: "sottolavNum-<ordineSottolavorazione>"

    */

    $('.'+classeElemento+'.'+ordineSottolav).each(function(){

        var totaleUs = $(this).children('td.tdCostoUs').text().split(' ')[1];
        var quantita=1;

        $(this).children('td.inputField').each(function(){
           quantita=quantita*parseFloat($(this).children('input').val());

        });

        totaleUs=parseFloat(totaleUs)*quantita;

        $(this).children('td.tdTotaleUs').html( "&euro; " + Math.round(totaleUs*100)/100 );

    });

    var totaleUsLavorazione = 0;
    var ordineLavorazione =classeElemento.split('_trSottolavorazione-')[1];

    $('.'+classeElemento ).each(function(){
        totaleUsLavorazione = totaleUsLavorazione+parseFloat($(this).children('td.tdTotaleUs').text().split(' ')[1]);

    });



    $('tr.trFoot'+ordineLavorazione).children('td.sumTotaliUs').html('&euro; '+totaleUsLavorazione);

}

/**********************************************************************************************/

var modificaQuantitaSottolavorazione = function($this){

    var classesOfRow = $this.parent().parent().attr('class').split(' ');

    var prezzoBase = parseFloat($this.parent().parent().children('td.tdCostoUnitario').text().split(' ')[1]);

    calcolaTotaleRigaSottolavorazione( classesOfRow[0], classesOfRow[1], prezzoBase );
    calcolaTotaleUs( classesOfRow[0], classesOfRow[1] );

    ordine = classesOfRow[0].split('_trSottolavorazione-')[1];
    var unitaMisura = $('.trFoot'+ordine).attr('class').split(' ')[2].split('-')[1];
    //unitaMisura = unitaMisura.split('_')[0]+' '+unitaMisura.split('_')[1];

    numero =parseFloat($this.val());
    variabile =$this.attr('class').split(' ')[2];


    if( !disabilitaSocketio ){
        socketPreventivo.emit("modifica_sottolavorazione", {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ordine' : ordine,
            'ordine_sottolavorazione' : classesOfRow[1].split('-')[1],
            'unitaMisura': unitaMisura,
            'fieldToChange' : variabile,
            'newValue' : numero
        });
    }
}

/********************************************************************************************/

var righeDimensioniSottolavorazione = function( unita, prezzoBase, numElement){

    if( unita == "cad" ){

        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'
    }
    else if ( unita == "ml" ){
        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' larghezza" type="number" step="0.01" name="L" placeholder="L" value=1.00></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'
    }
    else if ( unita == "mq" ){
        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' larghezza" type="number" step="0.01" name="L" placeholder="L" value=1.00></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' altezza" type="number" step="0.01" name="L" placeholder="H" value=1.00></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'
    }
    else if( unita == "mc" ){
        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' larghezza" type="number" step="0.01" name="L" placeholder="L" value=1.00></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' altezza" type="number" step="0.01" name="L" placeholder="H" value=1.00></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this))" class="numInput inputPrev-'+numElement+' profondita" type="number" step="0.01" name="L" placeholder="P" value=1.00></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'

    }
}


/***********************************************************************************************/
var countLavorazioniSettore = function(classSettore){
    var counter=0;
    $('tr[id^='+classSettore+'_trBody]').each(function(){
        counter++;
    });

    return counter;
}

/*****************************************************************************************/

var eliminaLavorazioneDaArrayAssistenze = function(idLav){

    var indexElToDel;

    $.each( arrayAssistenze, function(index, el){

        if( el[0] == idLav )
            indexElToDel = index;

    });

    arrayAssistenze.splice( indexElToDel, 1 );
}

/******************************************************************************************/

var eliminaLavorazione = function($this){

    var idElementToDel=$this.parent().parent().attr('id');
    var numEl = idElementToDel.split('_trBody-')[1];
    var classSettore =idElementToDel.split('_trBody-')[0];
    var numSettore = classSettore.split('-')[1];

    $('#'+idElementToDel).remove();
    $('.'+classSettore+'_trSottolavorazione-'+numEl).remove();
    $('.trFoot'+numEl).remove();

    $('#memoriaLavorazioniAggiunte-'+numSettore).children('div').each(function(){
        if( $(this).text() == 'aggiunto-'+numEl )
            $(this).remove();
    });

    $('.aggiunto-'+numEl).removeClass('aggiunto');
    $('.aggiunto-'+numEl).removeClass('aggiunto-'+numEl);

    eliminaLavorazioneDaArrayAssistenze( idElementToDel );

    if( !disabilitaSocketio ){
        socketPreventivo.emit("elimina_lavorazione",
                        {
                            "numero_preventivo" : numeroPreventivo,
                            "revisione" : revisionePreventivo,
                            "ordine": numEl,

                        }

        );
    }

    rienumeraPagina();


    calcolaTotaleParzialeSettore(classSettore);
    calcolaTotalePreventivo();


    // se non ci sono piu' lavorazioni per il relativo settore
    // elimina l'intestazione
    countLav = countLavorazioniSettore(classSettore);

    if( countLav == 0 ){

        $('.'+classSettore).each(function(){
            if($(this).hasClass('trHead'))
                $(this).remove();
        });

        $('.'+classSettore+'_head').remove();

    }

}

/*******************************************************************************************/

var eliminaSottolavorazione = function($this, unitaMisura){

    var sottolavorazioniCommonClass=$this.parent().parent().attr('class').split(' ')[0];
    var ordineLavorazione=sottolavorazioniCommonClass.split('_trSottolavorazione-')[1];
    var classSettore=sottolavorazioniCommonClass.split('_trSottolavorazione-')[0];

    $this.parent().parent().remove();


    var ordine_sottolavorazione=$this.parent().parent().attr('class').split(' ')[1].split('-')[1];

    if( !disabilitaSocketio ){
        socketPreventivo.emit("elimina_sottolavorazione",
            {
                "numero_preventivo" : numeroPreventivo,
                "revisione" : revisionePreventivo,
                "ordine": ordineLavorazione,
                "ordine_sottolavorazione": ordine_sottolavorazione

            }

        );
    }

    var $sottolavorazioni= $('.'+sottolavorazioniCommonClass);


    //rienumero i sottoelementi restanti e aggiorna il db
    var aux=0;
    $sottolavorazioni.each(function(){

        var oldOrder = $(this).attr('class').split(' ')[1].split('-')[1];

        if( !( typeof oldOrder === 'undefined') ){
            $(this).removeClass();
            $(this).addClass(sottolavorazioniCommonClass);
            $(this).addClass('sottolavNum-'+aux);

            if( !disabilitaSocketio ){
                socketPreventivo.emit("modifica_ordine_sottolavorazione",
                    {
                        "numero_preventivo" : numeroPreventivo,
                        "revisione" : revisionePreventivo,
                        "ordine": ordineLavorazione,
                        "oldOrdineSottolav": oldOrder,
                        "newOrdineSottolav": aux,
                        "unitaMisura": unitaMisura

                    }

                );
            }

            aux+=1;
        }
    });



    calcolaTotaleParziale(classSettore, ordineLavorazione);

    rienumeraPagina();

}

/********************************************************************************************/

var modificaNomeSottolavorazione = function($this){

    /* Modifico il nome della sottolavorazione nel database */
    var classRowSottolav = $this.parent().parent().attr('class').split(' ');

    var ordineLavorazione = classRowSottolav[0].split('_trSottolavorazione-')[1];
    var ordineSottolav = classRowSottolav[1].split('-')[1];
    var nome_modificato =  $this.parent().parent().children('.tdNomeSottolavorazione').children('textarea').val();

    if( !disabilitaSocketio ){
        socketPreventivo.emit("modifica_nome_sottolavorazione",
            {
                "numero_preventivo" : numeroPreventivo,
                "revisione" : revisionePreventivo,
                "ordine": ordineLavorazione,
                "ordine_sottolavorazione": ordineSottolav,
                "unitaMisura": $this.parent().parent().children('td.tdUnita').html(),
                "nome_modificato": nome_modificato


            });

    }

    var tmp = $this.parent().parent().attr('class').split(' ')[0].split('_trSottolavorazione-');

    var nome_originario = $('#'+tmp[0]+'_trBody-'+tmp[1]+ ' td.tdLavorazione').children('textarea').val();

    /* Trasformo la sottolavorazione in lavorazione se non lo è gia:
        -creo una nuova lavorazione
        -riordino */

/*
    if(!$('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).hasClass('trBody') && nome_originario != nome_modificato ){
        sottolavFirstCol = $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).children().first().html();

        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).children().first().addClass('firstCol');
        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).children().first().addClass('firstCol'+(ordineLavorazioni));
        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).children().first().html( '<label>'+(ordineLavorazioni)+'<label>');


        var costoUnitario = $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).children('td.tdCostoUnitario').html().split(' ')[1];
        var settore = classRowSottolav[0].split('_trSottolavorazione-')[0].split('-')[1];
        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).attr('id', 'settore-'+settore+'_trBody-'+(ordineLavorazioni));
        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).addClass('trBody');
        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).addClass('trSottolav');
        var nome_settore = $('.trHead.settore-'+0).children('.titleSettoreTd').first().html();

        /*registro una nuova lavorazione nel database*/
 /*       if( !disabilitaSocketio ){
            socketPreventivo.emit("add_nuova_lavorazione",
                {
                    "numero_preventivo" : numeroPreventivo,
                    "revisione" : revisionePreventivo,
                    "settore" : nome_settore,
                    "lavorazione" : $this.parent().parent().children('.tdNomeSottolavorazione').children('textarea').val(),
                    "unitaMisura" : $this.parent().parent().children('td.tdUnita').html(),
                    "ordine": ordineLavorazioni,
                    "prezzoUnitario" : costoUnitario

                }
             );
        }
*/

        /*rinumera tutte le lavorazione*/
  /*      rienumeraPagina();
        $('.'+classRowSottolav[0]+'.'+classRowSottolav[1]).children().first().append('<a onclick="eliminaSottolavorazione($(this), \'mq\')" class="delSottolavorazione fa fa-trash"></a>');
        $('.inputRicarico').trigger('input');

        ordineLavorazioni++;
    }*/

}

/*******************************************************************************************/

var aggiungiSottolavorazione = function($this, unitaMisura, costoLavorazione, costoUs, ricaricoAzienda, costoAssistenza, tipoCostoAssistenza ){

    var classSettore= $this.parent().parent().attr('id').split('_trBody-')[0];
    var numElement = $this.parent().parent().attr('id').split('_trBody-')[1];

    var nome_sottolavorazione = $this.parent().parent().children('td.tdLavorazione').children('textarea').val();

    var labelCostoAssistenza ='<label>';
    if( tipoCostoAssistenza ){
            labelCostoAssistenza += costoAssistenza +' %';
        }
        else
            labelCostoAssistenza += '&euro; '+ costoAssistenza;

    labelCostoAssistenza +='</label>';
    //var prezzoUnitario = prezzoUnitarioWithEuro.split(' ')[1];

    //Aggiungo una nuova riga prima del totale parziale ( rappresentato dalla classe trFoot )
    $('.trFoot'+numElement).before(
        '<tr class="'+classSettore+'_trSottolavorazione-'+numElement+'">'+
            '<td><a onclick="eliminaSottolavorazione($(this), \''+unitaMisura+'\')" class="delSottolavorazione fa fa-trash"></a></td>'+
            '<td class="tdPreventivo tdNomeSottolavorazione"><textarea oninput="modificaNomeSottolavorazione($(this))"></textarea></td>'+
            righeDimensioniSottolavorazione( unitaMisura, costoLavorazione, numElement)+
           '<td class="tdPreventivo tdUnita numColSmall">'+unitaMisura+'</td>'+
            '<td class="tdPreventivo tdCostoUnitario colSmall">&euro; '+costoLavorazione+'</td>'+
            '<td class="tdPreventivo tdCostoAssistenza">'+
                labelCostoAssistenza+
            '</td>'+
            '<td class="tdPreventivo tdCostoUs tdAdded">&euro; '+costoUs+'</td>'+
            '<td class="tdPreventivo tdTotaleUs tdAdded">&euro; '+costoUs+'</td>'+
            '<td class="tdPreventivo tdRicarico numColSmall tdAdded">+ <input oninput="modificaRicarico($(this))" type="number" min="0" max="100" class="inputRicarico" value="'+parseInt(ricaricoAzienda)+'">%</td>'+
            '<td class="totalSottolavorazione"></td>'+
        '</tr>'

    );

    if( cbxStatus ){
        $('.tdAdded').hide();
    }

    calcolaTotaleParziale(classSettore, numElement);

    //numero ogni "sottoriga aggiunta" e calcolo il totale della riga
    var aux=0;

    $('.'+classSettore+'_trSottolavorazione-'+numElement).each(function(){

        if( aux == 0 ){
            $(this).children('td.tdNomeSottolavorazione').children('textarea').remove();
        }

        calcolaTotaleUs(classSettore+'_trSottolavorazione-'+numElement, 'sottolavNum-'+aux);

        $(this).addClass('sottolavNum-'+aux);
        calcolaTotaleRigaSottolavorazione( classSettore+'_trSottolavorazione-'+numElement, 'sottolavNum-'+aux , costoLavorazione);
        aux+=1;

    });

    if( !disabilitaSocketio ){
        socketPreventivo.emit("add_nuova_sottolavorazione",
            {
                "numero_preventivo" : numeroPreventivo,
                "revisione" : revisionePreventivo,
                "ordine": numElement,
                "nome_modificato": ''
            }
        );
    }

    $('textarea').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    $('input').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });
}

/********************************************************************************************/
var modificaNomeLavorazione = function($this){

    var nuovoValore = $this.val();
    var ordineLav = $this.parent().parent().children('td.firstCol').children('label').text();
    var ordineSettore = $this.parent().parent().attr('id').split('_trBody-')[0].split('-')[1];

    var unitaMisura =$('tr.settore-'+ordineSettore+'_trSottolavorazione-'+ordineLav+'.sottolavNum-0').children('td.tdUnita').text();

    if( !disabilitaSocketio ){
        socketPreventivo.emit('modifica_nome_lavorazione', {

            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ordine_lavorazione' : ordineLav,
            'value' : nuovoValore,
            'unitaMisura' : unitaMisura

        });
    }
}

/*******************************************************************************************/

var modificaRicaricoGenerale = function($this){

    var nuovoRicarico = $this.val();
    var vecchioRicaricoGenerale = $this.attr('class').split('-')[1];

    $('.trBody').each(function(){
        var trBodyId = $(this).attr('id');
        var trBodySettore = trBodyId.split('_trBody-')[0].split('-')[1];
        var trBodyNum = trBodyId.split('_trBody-')[1];

        $('.settore-'+trBodySettore+'_trSottolavorazione-'+trBodyNum).each(function(){

            var ricaricoSottolav = $(this).children('td.tdRicarico').children('input').val();


            if( ricaricoSottolav == vecchioRicaricoGenerale ){

                $this.removeClass('ricaricoPrezzario-'+vecchioRicaricoGenerale);
                $this.addClass('ricaricoPrezzario-'+nuovoRicarico);
                $(this).children('td.tdRicarico').children('input').val(nuovoRicarico);
                $(this).children('td.tdRicarico').children('input').trigger('input');

            }


        });

    });

    if( !disabilitaSocketio ){
        socketPreventivo.emit('modifica_ricarico_generale', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ricarico': nuovoRicarico
        });

        socketPreventivo.emit('modifica_prezzi_cliente', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo
        });
    }

}

/*******************************************************************************************/

var modificaRicaricoExtra = function($this){

    var ricaricoExtra = parseInt($this.val());

    $('.trBody').each(function(){

        var idLavSplitted = $(this).attr('id').split('_trBody-');


        var classSottolav = idLavSplitted[0]+'_trSottolavorazione-'+idLavSplitted[1];

        $('.'+classSottolav).each(function(){

            $(this).children('td.tdRicarico').children('input').trigger('input');

        });

    });


    if( !disabilitaSocketio ){

        socketPreventivo.emit('modifica_prezzi_cliente', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo
        });
    }

}

/*******************************************************************************************/

var modificaRicarico = function($this){

    var costoUs = parseFloat($this.parent().parent().children('td.tdCostoUs').text().split(' ')[1]);
    var ricaricoGenerale = parseInt($this.val());
    var ricaricoExtra = parseInt($('#inputRicaricoExtra').val());

    var costoCliente = costoUs + (costoUs*ricaricoGenerale/100);

    costoCliente += costoCliente*ricaricoExtra/100;

    costoCliente = Math.round(costoCliente*100)/100;

    var classe1Sottolav =$this.parent().parent().attr('class').split(' ')[0];
    var classe2Sottolav =$this.parent().parent().attr('class').split(' ')[1];

    var ordineLav = classe1Sottolav.split('_trSottolavorazione-')[1];
    var ordineSottolav = classe2Sottolav.split('-')[1];

    var unitaMisura = $('tr.trFoot'+ordineLav).attr('class').split(' ')[2].split('-')[1];

    $this.parent().parent().children('td.tdCostoUnitario').html('&euro; '+costoCliente);
    calcolaTotaleRigaSottolavorazione(  classe1Sottolav, classe2Sottolav, costoCliente);

    if(!disabilitaSocketio){
        socketPreventivo.emit('modifica_ricarico_sottolav', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ordine_lavorazione' : ordineLav,
            'ordine_sottolav' : ordineSottolav,
            'unitaMisura' : unitaMisura,
            'prezzoBase' : costoCliente,
            'ricaricoGenerale' : ricaricoGenerale,
            'ricaricoExtra' : ricaricoExtra
        });
    }

}

/*******************************************************************************************/
/* funzione ausiliaria per modificaAssistenzaLavorazione()*/

var cambiaCostoAssistenza = function( labelCosto, classSottolavorazione ){

    $('.'+classSottolavorazione ).each(function(){

        $(this).children('.tdCostoAssistenza').html('<label>'+labelCosto+'</label>');
    });
}


/*******************************************************************************************/

var modificaCostoAssistenza = function($this){

    var newVal = $this.val();
    var typeCosto = $this.parent().children('div').children('input[type="radio"]:checked').val();
    var idContainer = $this.parent().parent().parent().attr('id');
    var idContainerSplitted = idContainer.split('_trBody-');
    var classSottolavorazione =  idContainerSplitted[0]+'_trSottolavorazione-'+idContainerSplitted[1];


    if( typeCosto == 'perc' )
        cambiaCostoAssistenza( newVal + ' %', classSottolavorazione);
    else
        cambiaCostoAssistenza( '&euro; '+ newVal, classSottolavorazione );

    $('.'+classSottolavorazione).each(function(){

        var class1 = $(this).attr('class').split(' ')[0];
        var class2 = $(this).attr('class').split(' ')[1];
        var costoUnitario = $(this).children('td.tdCostoUnitario').text().split(' ')[1];

        calcolaTotaleRigaSottolavorazione( class1, class2, costoUnitario);
    });

    if(!disabilitaSocketio){
        socketPreventivo.emit('modifica_assistenza_lavorazione', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ordine_lav' : idContainerSplitted[1],
            'toMod' : 'costo_assistenza',
            'newVal': newVal
        });
    }

}


/*******************************************************************************************/

var modificaTipoCostoAssistenza = function($this){

    var newTipo = $this.val();
    var costo = $this.parent().parent().children('input[type="number"]').val();

    var idContainer = $this.parent().parent().parent().parent().attr('id');
    var idContainerSplitted = idContainer.split('_trBody-');
    var classSottolavorazione =  idContainerSplitted[0]+'_trSottolavorazione-'+idContainerSplitted[1];

    if( newTipo == 'perc' )
        cambiaCostoAssistenza( costo + ' %', classSottolavorazione);
    else
        cambiaCostoAssistenza( '&euro; '+ costo, classSottolavorazione );

    $('.'+classSottolavorazione).each(function(){

        var class1 = $(this).attr('class').split(' ')[0];
        var class2 = $(this).attr('class').split(' ')[1];
        var costoUnitario = $(this).children('td.tdCostoUnitario').text().split(' ')[1];

        calcolaTotaleRigaSottolavorazione( class1, class2, costoUnitario);
    });

    if(!disabilitaSocketio){
        socketPreventivo.emit('modifica_assistenza_lavorazione', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ordine_lav' : idContainerSplitted[1],
            'toMod' : 'tipo_costo_assistenza',
            'newVal': newTipo
        });
    }

}


/*******************************************************************************************/

var modificaAssistenzaLavorazione = function($this){


    var idContainer = $this.parent().parent().parent().attr('id');
    var idContainerSplitted = idContainer.split('_trBody-');

    var classSottolavorazione =  idContainerSplitted[0]+'_trSottolavorazione-'+idContainerSplitted[1];

    var $tdCostoAssistenza = $this.parent().parent().parent().children('td.tdCostoAssistenza').children('div');
    var numberInputAssistenzaContainer = $('#'+idContainer+' td.tdCostoAssistenza').children('div');
    var radioInputAssistenzaContainer = $('#'+idContainer+' td.tdCostoAssistenza').children('div').children('div');

    var nomeAssistenza = $this.val();


    if( $this.val() == "No assistenza" ){
        $tdCostoAssistenza.hide();
        cambiaCostoAssistenza( '&euro; 0', classSottolavorazione );
        numberInputAssistenzaContainer.children('input[type="number"]').val(0);
        radioInputAssistenzaContainer.children('.radioPerc').trigger('click');
        nomeAssistenza = '';
    }
    else{
        $.each(arrayAssistenze, function(index, el){

            if( el[0] == idContainer ){
                if( el[1] == $this.val() ){
                    $tdCostoAssistenza.hide();
                    numberInputAssistenzaContainer.children('input[type="number"]').val(el[2]);

                    if( el[3] ){
                        cambiaCostoAssistenza( el[2] + ' %', classSottolavorazione);
                        radioInputAssistenzaContainer.children('.radioPerc').trigger('click');
                    }
                    else{
                        cambiaCostoAssistenza( '&euro; '+ el[2], classSottolavorazione );
                        radioInputAssistenzaContainer.children('.radioEuro').trigger('click');

                    }

                }
                else{
                    $tdCostoAssistenza.show();

                }

            }
        });
    }

    $('.'+classSottolavorazione).each(function(){

        var class1 = $(this).attr('class').split(' ')[0];
        var class2 = $(this).attr('class').split(' ')[1];
        var costoUnitario = $(this).children('td.tdCostoUnitario').text().split(' ')[1];

        calcolaTotaleRigaSottolavorazione( class1, class2, costoUnitario);
    });

    if(!disabilitaSocketio){
        socketPreventivo.emit('modifica_assistenza_lavorazione', {
            'numero_preventivo': numeroPreventivo,
            'revisione' : revisionePreventivo,
            'ordine_lav' : idContainerSplitted[1],
            'toMod' : 'assistenza',
            'newVal': nomeAssistenza
        });
    }

}


/*******************************************************************************************/

var selezionaSettoreLavCopia = function( $this, numeroPreventivoParametro, revisionePreventivoParametro, settore, tipologia, costoLavorazione, unitaMisura,
                                    nome_assistenza, costoAssistenza, tipoCostoAssistenza, assistenzeDistinte ){

    var settoriToPrint =[];

    settoriToPrint.push({value: settore, text: settore});


    $('#selectSettore option').each(function(){

        var classSettore = $(this).attr('class');

        if( $(this).text() != settore )
            settoriToPrint.push({value: classSettore, text: $(this).text()});
        else
            settoriToPrint[0]['value'] = classSettore;

    });

    swal.withFormAsync({
        title: 'Seleziona settore lavorazione copia:',
        showCancelButton: false,
        confirmButtonColor: '#DD6B55',
        confirmButtonText: 'Ok',
        cancelButtonText: 'annulla',
        closeOnConfirm: true,
        formFields: [

            { id: 'settore',
                type: 'select',
                options: settoriToPrint},


        ]
    }).then(function (context) {
        if(context._isConfirm){

            var ordine_lav_originale = $this.parent().parent().parent().attr('id').split('_trBody-')[1];

            aggiungiRigaCopia( numeroPreventivoParametro, revisionePreventivoParametro, settore, tipologia, costoLavorazione, unitaMisura,
                                    nome_assistenza, costoAssistenza, tipoCostoAssistenza, assistenzeDistinte, context.swalForm['settore'],
                                    ordine_lav_originale );
        }
    });


}


/*******************************************************************************************/

var aggiungiRigaCopia = function( numeroPreventivoParametro, revisionePreventivoParametro, settore, tipologia, costoLavorazione, unitaMisura,
                                    nome_assistenza, costoAssistenza, tipoCostoAssistenza, assistenzeDistinte, settoreSelected,
                                    ordine_lav_originale){


    var nomeSettoreSelected = $('#selectSettore option.'+settoreSelected).text();

    var idRow = aggiungiRiga(null, numeroPreventivoParametro, revisionePreventivoParametro, settore, tipologia,
                    costoLavorazione, unitaMisura, nome_assistenza, costoAssistenza,
                        tipoCostoAssistenza, assistenzeDistinte, true);
    /*Ricostruisco la riga costruita modificandone opportunamente id e classi in base al
        nuovo settore selezionato */

    var $rowLav =$('#'+idRow);
    var $rowSottolav = $rowLav.next();
    var $rowFoot = $rowSottolav.next();

    $rowLav.children('td.tdLavorazione').children('textarea').text('');
    $rowLav.children('td.tdLavorazione').children('div').children('select').val('No assistenza');
    $rowLav.children('td.tdLavorazione').children('div').children('select').trigger('change');

    var newLavId = settoreSelected + '_trBody-'+$rowLav.attr('id').split('_trBody-')[1];

    var sottolavArrayClasses = $rowSottolav.attr('class').split(' ');
    var sottolavFirstClass = sottolavArrayClasses[0];
    var sottolavOtherClassesArray = sottolavArrayClasses.slice(1, sottolavArrayClasses.length );
    var newSottolavFirstClass = settoreSelected + '_trSottolavorazione-' + sottolavFirstClass.split('_trSottolavorazione-')[1];


    var newLavClass = '';

    newLavClass = $rowLav.attr('class');

   /* $.each($rowLav.attr('class').split(' '), function(index, el){
        if( index+1 != $rowLav.attr('class').split(' ').length )
            newLavClass += el + ' ';


    });*/

    var newSottolavClass = newSottolavFirstClass + ' ';


    $.each(sottolavOtherClassesArray, function(index, el){

        if( index+1 == sottolavOtherClassesArray.length )
            newSottolavClass += el;
        else
            newSottolavClass += el + ' ';


    });

    var footArrayClasses = $rowFoot.attr('class').split(' ');

    var newFootClass = '';

    $.each(footArrayClasses, function(index, el){

        var spazio = ' ';

        if( index+1 == footArrayClasses.length )
            spazio = '';

        if( index == 1 )
            newFootClass += settoreSelected+'_trFoot'+spazio;
        else
            newFootClass += el+spazio;

    });

    var rowToMove = '<tr id="'+newLavId+'" class="'+newLavClass+'">'+$rowLav.html()+'</tr>'+
                    '<tr class="'+newSottolavClass+'">'+$rowSottolav.html()+'</tr>'+
                    '<tr class="'+newFootClass+'">'+$rowFoot.html()+'</tr>';


    var indexElToDel;
    $.each( arrayAssistenze, function(index, el){

        if( el[0] == idRow )
            indexElToDel = index;
    });
    arrayAssistenze.splice(indexElToDel, 1)

    arrayAssistenze.push([newLavId, 'No assistenza', 0, true]);



    var sezioneSettore =  $('#bodyPreventivo').children('.'+settoreSelected);

    //se non e' gia' stata aggiunta una sezione lo faccio e subito sotto metto la lavorazione
    // e il relativo footer
    if( !sezioneSettore.length ){

        var colspanNum = 10;

        if( !cbxStatus )
            colspanNum = 13;

        $('#bodyPreventivo').append(

            '<tr class="trHead '+settoreSelected+'">'+
                '<td  colspan="'+colspanNum+'"  class="titleSettoreTd">'+nomeSettoreSelected+'</td>'+
                '<td class="titleSettoreTd totaleSettore"></td>'+
            '</tr>'+
            '<tr class="trHead '+settoreSelected+'_head">'+
                '<th class="thPreventivo"></th>'+
                '<th class="thPreventivo"></th>'+
                '<th class="thPreventivo numColSmall">N</th>'+
                '<th class="thPreventivo numColSmall">L</th>'+
                '<th class="thPreventivo numColSmall">H</th>'+
                '<th class="thPreventivo numColSmall">P</th>'+
                '<th class="thPreventivo thQuantita">Quantità</th>'+
                '<th class="thPreventivo unitaClass">Unità</th>'+
                '<th class="thPreventivo thPrezzoUnitario">Prezzo unitario</th>'+
                '<th class="thPreventivo thCostoAssistenza">Prezzo Assistenza</th>'+
                '<th class="thPreventivo thAdded">Prezzo US</th>'+
                '<th class="thPreventivo thAdded">Totale US</th>'+
                '<th class="thPreventivo numColSmall thAdded">ricarico</th>'+
                '<th class="thPreventivo">Totale</th>'+
            '</tr>'+
            rowToMove

        );

    }
    else{
        $('.'+settoreSelected+'_trFoot').last().after(rowToMove);

    }

    if( cbxStatus ){
        $('.thAdded').hide();
        $('.tdAdded').hide();
    }

    var ricaricoAzienda = parseInt($('#inputRicaricoGenerale').val());
    var ricaricoExtra = parseInt($('#inputRicaricoExtra').val());

    costoLavorazione += (costoLavorazione*ricaricoAzienda/100);

    costoLavorazione += (costoLavorazione*ricaricoExtra/100);

    costoLavorazione = Math.round(costoLavorazione*100)/100;

    /*registro la riga nel database*/
    if( !disabilitaSocketio ){
        socketPreventivo.emit("add_nuova_lavorazione_copia",
            {
                "numero_preventivo" : numeroPreventivo,
                "revisione" : revisionePreventivo,
                "settore" : settore,
                "lavorazione" : tipologia,
                "unitaMisura" : unitaMisura,
                "ordine": ordineLavorazioni-1,
                "prezzoUnitario" : costoLavorazione,
                "nome_assistenza" : 'No assistenza',
                "costo_assistenza" : 0,
                "tipo_costo_assistenza" : true,
                "ordine_lav_originale" : ordine_lav_originale,
                "settore_lav_copia": nomeSettoreSelected

            }
         );
    }


   // ordineLavorazioni++;

    $rowLav.remove();
    $rowSottolav.remove();
    $rowFoot.remove();
    $('.settoreTmp').remove();

    rienumeraPagina();

    $('#'+newLavId).children('td.tdCostoAssistenza').children('div').children('input').val(0);
    $('#'+newLavId).children('td.tdCostoAssistenza').children('div').children('div').children('input.radioPerc').click();
    $('#'+newLavId).children('td.tdCostoAssistenza').children('div').children('input').trigger('input');

    $('#selectSettore option').each(function(){
        if( $(this).text() == settore )
            calcolaTotaleParzialeSettore($(this).attr('class'));
    });

    $('textarea').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    $('input').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    calcolaTotaleRigaSottolavorazione(settoreSelected, newLavId.split('_trBody-')[1]);

}

/*******************************************************************************************/

var aggiungiRiga= function($button, numeroPreventivoParametro, revisionePreventivoParametro, settore, tipologia, costoLavorazione, unitaMisura,
                            nome_assistenza, costoAssistenza, tipoCostoAssistenza, assistenzeDistinte, copia){

    /* copia e' un booleano che indica se stiamo copiando una lavorazione gia' aggiunta o meno */


    numeroPreventivo = numeroPreventivoParametro;
    revisionePreventivo = revisionePreventivoParametro;


    if( copia  || !$button.hasClass('aggiunto') ){

        var ricaricoAzienda = parseInt($('#inputRicaricoGenerale').val());
        var ricaricoExtra = parseInt($('#inputRicaricoExtra').val());

        var classSettore;

        if( !copia ){
            //Segno nel bottono cliccato che e' una lavorazione aggiunto
            $button.addClass("aggiunto");
            $button.addClass("aggiunto-"+ordineLavorazioni);

            classSettore = $button.attr('id').split('_')[0];
            var idSettore = parseInt($button.attr('id').split('_')[0].split('-')[1]);

            /*memorizzo nel apposita sezione l'aggiunta della classe "aggiunto-"+ordineLavorazioni al bottone*/
            $("#memoriaLavorazioniAggiunte-"+idSettore).append(
                '<div class="'+$button.attr('id')+'">'+
                    '<span class="classeToAdd">aggiunto-'+ordineLavorazioni+'</span>'+
                '</div>'

            );
        }
        else{
            $('#selectSettore option').each(function(){
                if( $(this).text() == settore )
                {
                    classSettore = $(this).attr('class');
                }

            });

        }

        costoUs = Math.round(costoLavorazione*100)/100;
        costoLavorazione += (costoLavorazione*ricaricoAzienda/100);

        costoLavorazione += (costoLavorazione*ricaricoExtra/100);

        costoLavorazione = Math.round(costoLavorazione*100)/100;

        var selectAssistenzeHtml = '<select onchange="modificaAssistenzaLavorazione($(this))">';


        $.each(assistenzeDistinte, function(index, el){
            selectAssistenzeHtml += '<option>'+el+'</option>';
        });

        selectAssistenzeHtml += '</select>';

        var labelCostoAssistenza = '<label>';

        if( tipoCostoAssistenza ){
            labelCostoAssistenza += costoAssistenza +' %';
        }
        else
            labelCostoAssistenza += '&euro; '+ costoAssistenza;

        labelCostoAssistenza +='</label>';

        arrayAssistenze.push([ classSettore+'_trBody-'+ordineLavorazioni, nome_assistenza, costoAssistenza, tipoCostoAssistenza ])

        var assistenzeDistinteParametro = '';

        $.each(assistenzeDistinte, function(index, el){
            assistenzeDistinteParametro += "\'"+ el + "\', ";

        });

        var parametriCopiaLavorazione = numeroPreventivoParametro+', '+revisionePreventivoParametro+', \''+
                                            settore+'\', \''+ tipologia +'\', '+costoUs+', \''+unitaMisura+'\', \''+
                                                nome_assistenza+'\', '+ costoAssistenza + ', '+ tipoCostoAssistenza +', ['+
                                                    assistenzeDistinteParametro+']';

        var extraClass;

        if(copia)
            extraClass = ' lavorazioneCopia';
        else
            extraClass = ''


        //Preparo la riga della lavorazione
        var rowsToAdd='<tr id="'+classSettore+'_trBody-'+ordineLavorazioni+'" class="trBody'+extraClass+'">'+
                        '<td class="firstCol'+ordineLavorazioni+' firstCol">'+
                            '<label></label>'+
                            '<a onclick="eliminaLavorazione($(this))" class="delElement fa fa-trash"></a>'+
                            '<a onclick="aggiungiSottolavorazione($(this), \''+unitaMisura+'\', '+costoLavorazione+', '+costoUs+', '+parseInt(ricaricoAzienda)+', '+costoAssistenza+', '+tipoCostoAssistenza+')" class="ctrButton addElement fa fa-plus"></a>'+
                            '<div>'+
                                '<a class="copiaLavorazione" onclick="selezionaSettoreLavCopia($(this), '+parametriCopiaLavorazione+');"> copia </a>'+
                            '</div>'+
                        '</td>'+
                        '<td class="tdPreventivo tdLavorazione">'+
                            '<textarea oninput="modificaNomeLavorazione($(this))" >'+tipologia+'</textarea>'+
                            '<div class="divNomeAssistenza"><label class="title">Assistenza:</label>'+selectAssistenzeHtml+'</div>'+
                        '</td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo tdCostoAssistenza">'+
                            '<div class="divCostoAssistenza" style="display:none">'+
                                '<input oninput="modificaCostoAssistenza($(this))" class="inputCostoAssistenza" type="number" value="'+costoAssistenza+'">'+
                                '<div>'+
                                '<input onclick="modificaTipoCostoAssistenza($(this))" class="radioPerc" type="radio" value="perc" name="'+classSettore+'_trBody-'+ordineLavorazioni+'">%</input>'+
                                '<input onclick="modificaTipoCostoAssistenza($(this))" class="radioEuro" type="radio" value="euro" name="'+classSettore+'_trBody-'+ordineLavorazioni+'">&euro;</input>'+
                                '</div>'+
                            '</div>'+
                        '</td>'+
                        '<td class="tdPreventivo tdAdded"></td>'+
                        '<td class="tdPreventivo prezzoBase tdAdded"></td>'+
                        '<td class="tdPreventivo numColSmall tdAdded"></td>'+
                        '<td class="tdPreventivo colSmall"></td>'+
                    '</tr>'+
                    '<tr class="'+classSettore+'_trSottolavorazione-'+ordineLavorazioni+' sottolavNum-0">'+
                            '<td></td>'+
                            '<td class="tdPreventivo tdNomeSottolavorazione"></td>'+
                            righeDimensioniSottolavorazione(  unitaMisura,
                                                              costoLavorazione,
                                                               ordineLavorazioni)+
                            '<td class="tdPreventivo tdUnita numColSmall">'+unitaMisura+'</td>'+
                            '<td class="tdPreventivo tdCostoUnitario colSmall">&euro; '+costoLavorazione+'</td>'+
                            '<td class="tdPreventivo tdCostoAssistenza">'+
                                labelCostoAssistenza+
                            '</td>'+
                            '<td class="tdPreventivo tdCostoUs tdAdded">&euro; '+costoUs+'</td>'+
                            '<td class="tdPreventivo tdTotaleUs tdAdded">&euro; '+costoUs+'</td>'+
                            '<td class="tdPreventivo tdRicarico numColSmall tdAdded">+ <input oninput="modificaRicarico($(this))" type="number" min="0" max="100" class="inputRicarico" value="'+parseInt(ricaricoAzienda)+'">%</td>'+
                            '<td class="totalSottolavorazione"></td>'+
                    '</tr>'+
                    '<tr class="trFoot '+classSettore+'_trFoot unitaMisura-'+ unitaMisura +' trFoot'+parseInt(ordineLavorazioni)+'">'+
                            '<td colspan="6"></td>'+
                            '<td class="quantita colSmall"></td>'+
                            '<td>'+unitaMisura+'</td>'+
                            '<td colSmall"></td>'+
                            '<td class="tdPreventivo"></td>'+
                            '<td class="tdPreventivo tdAdded"></td>'+
                            '<td class="tdPreventivo tdAdded sumTotaliUs"></td>'+
                            '<td class="tdPreventivo tdAdded"></td>'+
                            '<td class="footTot"></td>'+
                     '</tr>';

        var sezioneSettore =  $('#bodyPreventivo').children('.'+classSettore);

        //se non e' gia' stata aggiunta una sezione lo faccio e subito sotto metto la lavorazione
        // e il relativo footer
        if( !sezioneSettore.length ){

            var colspanNum = 10;

            if( !cbxStatus )
                colspanNum = 13;

            var classSettoreCopia = '';

            if(copia)
                classSettoreCopia = ' settoreTmp'

            $('#bodyPreventivo').append(

                '<tr class="trHead '+classSettore+classSettoreCopia+'">'+
                    '<td  colspan="'+colspanNum+'"  class="titleSettoreTd">'+settore+'</td>'+
                    '<td class="titleSettoreTd totaleSettore"></td>'+
                '</tr>'+
                '<tr class="trHead '+classSettore+'_head'+classSettoreCopia+'">'+
                    '<th class="thPreventivo"></th>'+
                    '<th class="thPreventivo"></th>'+
                    '<th class="thPreventivo numColSmall">N</th>'+
                    '<th class="thPreventivo numColSmall">L</th>'+
                    '<th class="thPreventivo numColSmall">H</th>'+
                    '<th class="thPreventivo numColSmall">P</th>'+
                    '<th class="thPreventivo thQuantita">Quantità</th>'+
                    '<th class="thPreventivo unitaClass">Unità</th>'+
                    '<th class="thPreventivo thPrezzoUnitario">Prezzo unitario</th>'+
                    '<th class="thPreventivo thCostoAssistenza">Prezzo Assistenza</th>'+
                    '<th class="thPreventivo thAdded">Prezzo US</th>'+
                    '<th class="thPreventivo thAdded">Totale US</th>'+
                    '<th class="thPreventivo numColSmall thAdded">ricarico</th>'+
                    '<th class="thPreventivo">Totale <br/> Cliente</th>'+
                '</tr>'+
                rowsToAdd

            );

        }
        else{
            $('.'+classSettore+'_trFoot').last().after( rowsToAdd );
        }

        /*seleziono l'assistenza correttamente*/

        $('#'+classSettore+'_trBody-'+ordineLavorazioni+' td.tdLavorazione' ).children('div.divNomeAssistenza').children('select').val(nome_assistenza);
        $('#'+classSettore+'_trBody-'+ordineLavorazioni+' td.tdLavorazione').children('div.divNomeAssistenza').children('select').trigger('change')

        var radioAssistenzaContainer = $('#'+classSettore+'_trBody-'+ordineLavorazioni+' td.tdCostoAssistenza').children('div');

       /* if( tipoCostoAssistenza )
            radioAssistenzaContainer.children('.radioPerc').trigger('click');
        else
            radioAssistenzaContainer.children('.radioEuro').trigger('click');*/

        if( cbxStatus ){
            $('.thAdded').hide();
            $('.tdAdded').hide();
        }

        calcolaTotaleRigaSottolavorazione(classSettore+'_trSottolavorazione-'+ordineLavorazioni, 'sottolavNum-0', costoLavorazione );
        calcolaTotaleUs(classSettore+'_trSottolavorazione-'+ordineLavorazioni, 'sottolavNum-0');

        /*registro la riga nel database*/
        if( !disabilitaSocketio && !copia ){
            socketPreventivo.emit("add_nuova_lavorazione",
                {
                    "numero_preventivo" : numeroPreventivo,
                    "revisione" : revisionePreventivo,
                    "settore" : settore,
                    "lavorazione" : tipologia,
                    "unitaMisura" : unitaMisura,
                    "ordine": ordineLavorazioni,
                    "prezzoUnitario" : costoLavorazione,
                    "nome_assistenza" : nome_assistenza,
                    "costo_assistenza" : costoAssistenza,
                    "tipo_costo_assistenza" : tipoCostoAssistenza

                }
             );
        }


        /*ad ogni nuova aggiunta di elemento rinumera tuttoquanto*/
        if(!copia)
            rienumeraPagina();

        $('.inputRicarico').trigger('input');

       // lavToCtrl.push([classSettore+'_trBody-'+ordineLavorazioni, settore]);

        ordineLavorazioni++;
    }

    $('textarea').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    $('input').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    return classSettore+'_trBody-'+(ordineLavorazioni-1);
}

/*********************************************************************************/

var aggiungiSettoriELavorazioni = function(listaLavorazioni){
    /* gli elementi di listaLavorazioni sono array con in prima posizione il nome del settore
        e in seconda la lista delle lavorazioni associate */

    var counterSettori = 0;
    listaLavorazioni.forEach(function(settoreELav){

        $('#selectSettore').append('<option class="settore-'+counterSettori+'">'+settoreELav[0]+'</option>');

        $('#memoriaLavorazioniAggiunte').append(
             '<div id="memoriaLavorazioniAggiunte-'+counterSettori+'" class="settoreMemorizzato"></div>'
        );

        var counterLavorazioni = 1;

        settoreELav[1].forEach(function(lavorazione){
            $('#listaElementFattura').append(
                 '<li><button id="settore-'+counterSettori+'_lav-'+counterLavorazioni+'" class="elementFattura"><label for="settore-'+counterSettori+'_lav-'+counterLavorazioni+'">'+lavorazione+'</label></button></li>'
            );

            counterLavorazioni++;
        });


        counterSettori++;
    });

}

/**********************************************************************************/
var settaDisabilitaSocketio = function(value){
    //value è un booleano

    disabilitaSocketio = value;
}

/**********************************************************************************/

var showLavorazioniPerSettore = function(settoreClass){

    $('#listaElementFattura').children('li').each(function(){

        var idButton = $(this).children('button').attr('id').split('_')[0];

        if( idButton == settoreClass ){
            $(this).show();
        }
        else{
            $(this).hide();
        }
    });
}

/**********************************************************************************/

var trovaClassSettore = function(settore){

    var toRet;

    $('#selectSettore option').each(function(){
        if( $(this).text() == settore )
            toRet = $(this).attr('class');
    });

    return toRet;
}

/***********************************************************************************/

var trovaIdButtonLavorazione = function(classSettore, tipologia_lavorazione){

    var toRet;

    $('button[id^='+classSettore+']').each(function(){

        if($(this).text() == tipologia_lavorazione )
            toRet = $(this).attr('id');
    });

    return toRet;
}

/**********************************************************************************/
$(function(){

    $('#selectSettore option:selected').each(function(){
        showLavorazioniPerSettore($(this).attr('class'));
    });

    $('#selectSettore').change(function(){
        $(this).children('option:selected').each(function(){
            showLavorazioniPerSettore($(this).attr('class'));
        });
    });
});