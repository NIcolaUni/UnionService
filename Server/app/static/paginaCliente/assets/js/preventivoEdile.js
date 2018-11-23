/************************************************************************************************/
var numeroPreventivo;
var dataPreventivo;
/* variabile globale usata per tener conto del numero dell'ultima lavorazione aggiunta */
var ordineLavorazioni = 1;

var disabilitaSocketio = false;

/************************************************************************************************/

function rienumeraMemoriaLavorazioni(){

    var counter = 1;
    $('#memoriaLavorazioniAggiunte').children('.settoreMemorizzato').each(function(){
        $(this).children('div').each(function(){
            $(this).text('aggiunto-'+counter);
            counter+=1;
        });

    });
}


/************************************************************************************************/

var rienumeraPagina = function(numeroPreventivo, dataPreventivo, ){

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

        /*modifico i pulsanti "aggiungi elemento" degli elementi presenti*/
        $('.aggiunto-'+oldNum).addClass('aggiunto-old'+oldNum);
        $('.aggiunto-'+oldNum).removeClass('aggiunto-'+oldNum);


    });


    /*effettuo l'effettiva rienumerazione*/
    $('.trBody').each(function(){
        var classSettore = $(this).attr('id').split('_trBody-')[0];

        oldNum =  $(this).attr('id').split('-old')[1];

        $('.aggiunto-old'+oldNum).addClass('aggiunto-'+counter);
        $('.aggiunto-old'+oldNum).removeClass('aggiunto-old'+oldNum);

        $(this).attr('id', classSettore+'_trBody-'+counter);

        $(this).children('.firstCol-old'+oldNum).addClass('firstCol'+counter);
        $(this).children('.firstCol-old'+oldNum).removeClass('firstCol-old'+oldNum);

        $(this).children('.firstCol'+counter).children('label').text(counter);
        $(this).children('.firstCol'+counter).children('.add-old'+oldNum).addClass('add-'+counter);
        $(this).children('.firstCol'+counter).children('.add-old'+oldNum).removeClass('add-old'+oldNum);


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

        var unitaMisura = $('.trFoot'+counter).attr('class').split(' ')[2].split('-')[1];
        //unitaMisura = unitaMisura.split('_')[0]+' '+unitaMisura.split('_')[1];

        if( !disabilitaSocketio ){
            socketPreventivo.emit("modifica_ordine_lavorazione",
                            {
                                "numero_preventivo" : numeroPreventivo,
                                "data" : dataPreventivo,
                                "unitaMisura" : unitaMisura,
                                "ordineVecchio": oldNum,
                                "ordineNuovo" : counter

                            }
                  );
        }
        counter+=1;
    });



    rienumeraMemoriaLavorazioni();

}


/***********************************************************************************************/

var calcolaTotalePreventivo = function(){
    var totale = 0;

    $('.trBody').each(function(){
            var numEl = $(this).attr('id').split('_trBody-')[1];
            totale+=parseFloat($('.trFoot'+numEl).children('.footTot').text().split(' ')[1]);

    });

    $('#divTotale').html('<span><u>Totale:</u> &euro; ' + Math.round(totale*100)/100 + '</span>' );
}


/***********************************************************************************************/

var calcolaTotaleParzialeSettore = function( classSettore ){
    totale = 0;

    $("."+classSettore+"_trFoot").each(function(){
        totale += parseFloat($(this).children('.footTot').text().split(' ')[1]);

    });

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

    $('.'+classeElemento+'.'+ordineSottolav).each(function(){


        var totalePrezzo=prezzoBase;
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

/**********************************************************************************************/

var modificaQuantitaSottolavorazione = function($this, prezzoBase){

    var classesOfRow = $this.parent().parent().attr('class').split(' ');
    calcolaTotaleRigaSottolavorazione( classesOfRow[0], classesOfRow[1], prezzoBase );

    ordine = classesOfRow[0].split('_trSottolavorazione-')[1];
    var unitaMisura = $('.trFoot'+ordine).attr('class').split(' ')[2].split('-')[1];
    //unitaMisura = unitaMisura.split('_')[0]+' '+unitaMisura.split('_')[1];

    numero =parseFloat($this.val());
    variabile =$this.attr('class').split(' ')[2];

    if( !disabilitaSocketio ){
        socketPreventivo.emit("modifica_sottolavorazione", {
            'numero_preventivo': numeroPreventivo,
            'data' : dataPreventivo,
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

        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'
    }
    else if ( unita == "ml" ){
        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' larghezza" type="number" step="0.01" name="L" placeholder="L" value=1.00></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'
    }
    else if ( unita == "mq" ){
        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' larghezza" type="number" step="0.01" name="L" placeholder="L" value=1.00></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' altezza" type="number" step="0.01" name="L" placeholder="H" value=1.00></td>'+
                '<td class="tdPreventivo numColSmall"></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'
    }
    else if( unita == "mc" ){
        return  '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' numero" type="number" name="numero" placeholder="numero" value=1></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' larghezza" type="number" step="0.01" name="L" placeholder="L" value=1.00></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' altezza" type="number" step="0.01" name="L" placeholder="H" value=1.00></td>'+
                '<td class="tdPreventivo inputField numColSmall basePrezzo-'+prezzoBase+' inputPrev"><input oninput="modificaQuantitaSottolavorazione($(this), '+ prezzoBase +')" class="numInput inputPrev-'+numElement+' profondita" type="number" step="0.01" name="L" placeholder="P" value=1.00></td>'+
                '<td class="tdPreventivo totDimensioni colSmall"></td>'

    }
}

/*********************************************************************************************/

var settaLastElement = function(classSettore){

    $('tr[id^='+classSettore+'_trBody]').last().addClass(classSettore+'_lastAdded');

}

/***********************************************************************************************/
var countLavorazioniSettore = function(classSettore){
    var counter=0;
    $('tr[id^='+classSettore+'_trBody]').each(function(){
        counter++;
    });

    return counter;
}


/******************************************************************************************/

var eliminaLavorazione = function($this){

    var idElementToDel=$this.parent().parent().attr('id');
    var numEl = idElementToDel.split('_trBody-')[1];
    var classSettore =idElementToDel.split('_trBody-')[0];
    var lastEl = $('#'+idElementToDel).hasClass(classSettore+'_lastAdded'); //variabile booleana


    $('#'+idElementToDel).remove();
    $('.'+classSettore+'_trSottolavorazione-'+numEl).remove();
    $('.trFoot'+numEl).remove();

    $('#memoriaLavorazioniAggiunte-'+classSettore).children('div').each(function(){
        if( $(this).text() == 'aggiunto-'+numEl )
            $(this).remove();
    });

    $('.aggiunto-'+numEl).removeClass('aggiunto');
    $('.aggiunto-'+numEl).removeClass('aggiunto-'+numEl);

    if( !disabilitaSocketio ){
        socketPreventivo.emit("elimina_lavorazione",
                        {
                            "numero_preventivo" : numeroPreventivo,
                            "data" : dataPreventivo,
                            "ordine": numEl,

                        }

        );
    }

    rienumeraPagina();

    if( lastEl ){
        settaLastElement(classSettore);
    }

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
                "data" : dataPreventivo,
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
                        "data" : dataPreventivo,
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



}

/*******************************************************************************************/

var aggiungiSottolavorazione = function($this, unitaMisura, costoLavorazione){

    var classSettore= $this.parent().parent().attr('id').split('_trBody-')[0];
    var numElement = $this.parent().parent().attr('id').split('_trBody-')[1];

    //var prezzoUnitario = prezzoUnitarioWithEuro.split(' ')[1];

    //Aggiungo una nuova riga prima del totale parziale ( rappresentato dalla classe trFoot )
    $('.trFoot'+numElement).before(
        '<tr class="'+classSettore+'_trSottolavorazione-'+numElement+'">'+
            '<td colspan="2"><a onclick="eliminaSottolavorazione($(this), \''+unitaMisura+'\')" class="delSottolavorazione fa fa-trash"></a></td>'+
            righeDimensioniSottolavorazione( unitaMisura, costoLavorazione, numElement)+
           '<td class="tdPreventivo numColSmall">'+unitaMisura+'</td>'+
            '<td class="tdPreventivo colSmall">&euro; '+costoLavorazione+'</td>'+
            '<td class="totalSottolavorazione"></td>'+
        '</tr>'

    );

    calcolaTotaleParziale(classSettore, numElement);

    //numero ogni "sottoriga aggiunta" e calcolo il totale della riga
    var aux=0;

    $('.'+classSettore+'_trSottolavorazione-'+numElement).each(function(){

        $(this).addClass('sottolavNum-'+aux);
        calcolaTotaleRigaSottolavorazione( classSettore+'_trSottolavorazione-'+numElement, 'sottolavNum-'+aux , costoLavorazione);
        aux+=1;
    });

    if( !disabilitaSocketio ){
        socketPreventivo.emit("add_nuova_sottolavorazione",
            {
                "numero_preventivo" : numeroPreventivo,
                "data" : dataPreventivo,
                "ordine": numElement

            }

        );
    }

}

/*******************************************************************************************/

var aggiungiRiga= function($button, numeroPreventivoParametro, dataPreventivoParametro, settore, tipologia, costoLavorazione, ricaricoAzienda, unitaMisura ){


    numeroPreventivo = numeroPreventivoParametro;
    dataPreventivo = dataPreventivoParametro;

    if( !$button.hasClass('aggiunto') ){

        //Segno nel bottono cliccato che e' una lavorazione aggiunto
        $button.addClass("aggiunto");
        $button.addClass("aggiunto-"+ordineLavorazioni);

        var classSettore = $button.attr('id').split('_')[0];
        var idSettore = parseInt($button.attr('id').split('_')[0].split('-')[1]);

        /*memorizzo nel apposita sezione l'aggiunta della classe "aggiunto-"+ordineLavorazioni al bottone*/
        $("#memoriaLavorazioniAggiunte-"+idSettore).append(
            '<div class="'+$button.attr('id')+'">'+
                '<span class="classeToAdd">aggiunto-'+ordineLavorazioni+'</span>'+
            '</div>'

        );

        costoLavorazione = costoLavorazione+(costoLavorazione*ricaricoAzienda/100);


        //Preparo la riga della lavorazione
        var rowsToAdd='<tr id="'+classSettore+'_trBody-'+ordineLavorazioni+'" class="trBody '+classSettore+'_lastAdded">'+
                        '<td class="firstCol'+ordineLavorazioni+' firstCol">'+
                            '<label></label>'+
                            '<a onclick="eliminaLavorazione($(this))" class="delElement fa fa-trash"></a>'+
                            '<a onclick="aggiungiSottolavorazione($(this), \''+unitaMisura+'\', '+costoLavorazione+')" class="ctrButton addElement fa fa-plus"></a>'+
                        '</td>'+
                        '<td class="tdPreventivo tdLavorazione"><textarea>'+tipologia+'</textarea></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo numColSmall"></td>'+
                        '<td class="tdPreventivo prezzoBase colSmall"></td>'+
                        '<td></td>'+
                    '</tr>'+
                    '<tr class="'+classSettore+'_trSottolavorazione-'+ordineLavorazioni+' sottolavNum-0">'+
                            '<td colspan="2"><a onclick="eliminaSottolavorazione($(this), \''+unitaMisura+'\')" class="delSottolavorazione fa fa-trash"></a></td>'+
                            righeDimensioniSottolavorazione(  unitaMisura,
                                                              costoLavorazione,
                                                               ordineLavorazioni)+
                            '<td class="tdPreventivo numColSmall">'+unitaMisura+'</td>'+
                            '<td class="tdPreventivo colSmall">&euro; '+costoLavorazione+'</td>'+
                            '<td class="totalSottolavorazione"></td>'+
                    '</tr>'+
                    '<tr class="trFoot '+classSettore+'_trFoot unitaMisura-'+ unitaMisura +' trFoot'+parseInt(ordineLavorazioni)+'">'+
                            '<td colspan="6"></td>'+
                            '<td class="quantita colSmall"></td>'+
                            '<td>'+unitaMisura+'</td>'+
                            '<td colSmall"></td>'+
                            '<td class="footTot"></td>'+
                     '</tr>';

        var sezioneSettore =  $('#bodyPreventivo').children('.'+classSettore);

        //se non e' gia' stata aggiunta una sezione lo faccio e subito sotto metto la lavorazione
        // e il relativo footer
        if( !sezioneSettore.length ){

            $('#bodyPreventivo').append(

                '<tr class="trHead '+classSettore+'">'+
                    '<td  colspan="9"  class="titleSettoreTd">'+settore+'</td>'+
                    '<td class="titleSettoreTd totaleSettore"></td>'+
                '</tr>'+
                '<tr class="trHead '+classSettore+'_head">'+
                    '<th class="thPreventivo"></th>'+
                    '<th class="thPreventivo"></th>'+
                    '<th class="thPreventivo numColSmall">N</th>'+
                    '<th class="thPreventivo numColSmall">L</th>'+
                    '<th class="thPreventivo numColSmall">H</th>'+
                    '<th class="thPreventivo numColSmall">P</th>'+
                    '<th class="thPreventivo colSmall">Quantità</th>'+
                    '<th class="thPreventivo numColSmall">Unità</th>'+
                    '<th class="thPreventivo colSmall">Prezzo unitario</th>'+
                    '<th class="thPreventivo">Totale</th>'+
                '</tr>'+
                rowsToAdd

            );

        }
        else{

            $("."+classSettore+"_lastAdded").removeClass(classSettore+"_lastAdded");
            $('.'+classSettore+'_trFoot').last().after( rowsToAdd );

        }

        calcolaTotaleRigaSottolavorazione(classSettore+'_trSottolavorazione-'+ordineLavorazioni, 'sottolavNum-0', costoLavorazione );

        /*registro la riga nel database*/
        if( !disabilitaSocketio ){
            socketPreventivo.emit("add_nuova_lavorazione",
                {
                    "numero_preventivo" : numeroPreventivo,
                    "data" : dataPreventivo,
                    "settore" : settore,
                    "lavorazione" : tipologia,
                    "unitaMisura" : unitaMisura,
                    "ordine": ordineLavorazioni,
                    "prezzoUnitario" : costoLavorazione

                }
             );
        }


        /*ad ogni nuova aggiunta di elemento rinumera tuttoquanto*/
        rienumeraPagina(numeroPreventivo, dataPreventivo);

        ordineLavorazioni++;
    }


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

        var counterLavorazioni = 0;

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