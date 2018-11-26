
var ordineProdotti = 1; // variabile globale usata per tener conto del numero dell'ultimo prodotto aggiunto
var numeroPreventivo;
var dataPreventivo;
var cbxStatus=true;

/********************************************************************************************/

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
            { id: 'sumisura', label: 'Preventivo su misura', name: 'sumisura', value: 'sumisura', type: 'checkbox' },
            { id: 'chiudi', label: 'Chiudi preventivo', name: 'chiudi', value: 'chiudi', type: 'checkbox' },

        ]
    }).then(function (context) {
        if(context._isConfirm){

            var sceltaSconto=parseInt(context.swalForm['scontoTipo']);
            var chiudiPrev=false;
            var sumisura=false;
            var iva=parseInt(context.swalForm['iva']);

            console.log( 'sto stampando: ' + iva );
            if( context.swalForm['scontoTipo'] == 'chiudi' )
                chiudiPrev=true;

            if( context.swalForm['sumisura'] == 'sumisura' )
                sumisura=true;

            if( sceltaSconto == 1 ){
                socketFiniture.emit('stampa_preventivo', {
                                                'dip': usernameDip,
                                                'numero_preventivo': numeroPreventivo,
                                                'data': dataPreventivo,
                                                'iva': iva,
                                                'tipoSconto': sceltaSconto,
                                                'sconto': 0,
                                                'chiudiPreventivo': chiudiPrev,
                                                'sumisura': sumisura });
                sweetAlert.close();
            }
            else{
                var toPrint="";

                if( sceltaSconto == 2 ){
                    toPrint ="Inserire sconto netto da applicare:";
                }
                else if( sceltaSconto == 3 ){
                    toPrint ="Inserire sconto percentuale da applicare:";
                }
                else if( sceltaSconto == 4 ){
                    toPrint = "Forza totale:";
                }



                swal.withFormAsync({
                    title: toPrint,
                    showCancelButton: true,
                    confirmButtonColor: '#DD6B55',
                    confirmButtonText: 'Ok',
                    cancelButtonText: 'annulla',
                    closeOnConfirm: true,
                    formFields: [

                        { id: 'sconto', label: 'Sconto: ', name: 'sconto', type: 'number', placeholder: 'sconto', value: '0' },


                    ]
                }).then(function (context) {
                    if(context._isConfirm){
                         socketFiniture.emit('stampa_preventivo', {
                                                'dip': usernameDip,
                                                'numero_preventivo': numeroPreventivo,
                                                'data': dataPreventivo,
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

/********************************************************************************************/

var aggiungiNote = function($this){

    socketFiniture.emit('inserisci_note', {   'numero_preventivo': numeroPreventivo,
                                                        'data': dataPreventivo,
                                                        'nota': $this.val() });
}

/********************************************************************************************/

var espandiTabella = function(){

    if(cbxStatus == true ){

        $('.titleTipologiaTd').attr('colspan', 9 );
        $('.thAdded').show();
        $('.tdAdded').show();
        cbxStatus=false;
    }
    else{

        $('.titleTipologiaTd').attr('colspan', 7 );
        $('.thAdded').hide();
        $('.tdAdded').hide();
        cbxStatus=true;

    }
}

/********************************************************************************************/

var calcolaTotalePreventivo = function(){

    var totale =0;
    $('.tdDiffCapitolato').each(function(){
        var costo = $(this).html();

        if( costo == "-" ){

            costo = 0;
        }
        else {
            costo = parseFloat(costo.split(' ')[1]);
        }

        totale += costo;
    });

    $('#divTotale').html("<span> <u>Totale: </u> &euro; "+ Math.round(totale*100)/100 +"</span>");
}


/********************************************************************************************/

var modificaQuantitaProdotto = function( $inputQuantita, diffCapitolato ){

    var quantitaValue = parseFloat( $inputQuantita.val() );
    var newCap = 0;

    if( diffCap != '-' )
    {
        newCap = Math.round(diffCap*quantitaValue*100)/100;

        if( newCap == 0 )
            $inputQuantita.parent().parent().children('td.tdDiffCapitolato').html('-');
        else
            $inputQuantita.parent().parent().children('td.tdDiffCapitolato').html('&euro; '+newCap);



        calcolaTotalePreventivo();

        var ordineProdotto = $inputQuantita.parent().parent().attr('id').split('_trBody-')[1];

        socketFiniture.emit("modifica_prodotto",
                        {
                            "numero_preventivo" : numeroPreventivo,
                            "data" : dataPreventivo,
                            "ordine": ordineProdotto,
                            "quantita": quantitaValue,
                            "diffCapitolato": newCap

                        }
        );

    }


}

/********************************************************************************************/

var rienumeraMemoriaLavorazioni = function(){

    var counter = 1;
    $('#memoriaProdottiAggiunti').children('.tipologiaMemorizzata').each(function(){
        $(this).children('div').each(function(){
            $(this).text('aggiunto-'+counter);
            counter+=1;
        });

    });
}


/********************************************************************************************/

var rienumeraPagina = function(){

    var counter = 1;
    var oldNum="";

    //rinomino tutti gli id degli elementi per non rischiare di
    //averne due uguali nella renumerazione.
    $('.trBody').each(function(){
        var idTrBodySplitted = $(this).attr('id').split('_trBody-');
        var tipologia=idTrBodySplitted[0];



        oldNum = idTrBodySplitted[1]

        $(this).attr('id', tipologia+'-old_trBody-'+oldNum);

        $(this).children('.firstCol'+oldNum).addClass('firstCol-old'+oldNum);
        $(this).children('.firstCol'+oldNum).removeClass('firstCol'+oldNum);

        /*modifico i pulsanti "aggiungi elemento" degli elementi presenti*/
        $('.aggiunto-'+oldNum).addClass('aggiunto-old'+oldNum);
        $('.aggiunto-'+oldNum).removeClass('aggiunto-'+oldNum);
    });


    $('.trBody').each(function(){

        var idTrBodySplitted = $(this).attr('id').split('-old_trBody-');
        var tipologia=idTrBodySplitted[0];
        oldNum = idTrBodySplitted[1]


        $('.aggiunto-old'+oldNum).addClass('aggiunto-'+counter);
        $('.aggiunto-old'+oldNum).removeClass('aggiunto-old'+oldNum);

        $(this).attr('id', tipologia+'_trBody-'+counter);

        $(this).children('.firstCol-old'+oldNum).addClass('firstCol'+counter);
        $(this).children('.firstCol-old'+oldNum).removeClass('firstCol-old'+oldNum);

        $(this).children('.firstCol'+counter).children('label').text(counter);



        socketFiniture.emit("modifica_ordine_prodotto",
                        {
                            "numero_preventivo" : numeroPreventivo,
                            "data" : dataPreventivo,
                            "ordineVecchio": -oldNum,
                            "ordineNuovo" : counter

                        }
              );
        counter+=1;
    });

    rienumeraMemoriaLavorazioni();

}

/********************************************************************************************/

var settaLastElement = function(tipologia){

    $('tr[id^='+tipologia+'_trBody]').last().addClass(tipologia+'_lastAdded');
}

/********************************************************************************************/

var countProdottiPerTipologia = function(tipologia){
        var counter=0;
        $('tr[id^='+tipologia+'_trBody]').each(function(){
            counter++;
        });

        return counter;
}


/********************************************************************************************/

var cancellaProdotto = function( $delBtn ){

    var idElementToDel=$delBtn.parent().parent().attr('id');
    var numEl = idElementToDel.split('_trBody-')[1];
    var tipologia =idElementToDel.split('_trBody-')[0];
    var lastEl = $('#'+idElementToDel).hasClass(tipologia+'_lastAdded'); //variabile booleana

    var idTipologia = tipologia.split('-')[1];

    $('#'+idElementToDel).remove();

    $('#memoriaProdottiAggiunti-'+idTipologia).children('div').each(function(){
        if( $(this).children('span').text() == 'aggiunto-'+numEl )
            $(this).remove();
    });

    $('.aggiunto-'+numEl).removeClass('aggiunto');
    $('.aggiunto-'+numEl).removeClass('aggiunto-'+numEl);

    socketFiniture.emit("elimina_prodotto",
                    {
                        "numero_preventivo" : numeroPreventivo,
                        "data" : dataPreventivo,
                        "ordine": numEl,

                    }

    );

    rienumeraPagina();

    if( lastEl ){
        settaLastElement(tipologia);
    }

    // se non ci sono piu' prodotti per la relativo tipologia
    // elimina l'intestazione
    countProd = countProdottiPerTipologia(tipologia);

    if( countProd == 0 ){

        $('.trHead.'+tipologia).remove();

        $('.trHead.'+tipologia+'_head').remove();

    }

}

/********************************************************************************************/
var aggiungiRiga = function($button, numeroPreventivoParametro, dataPreventivoParametro, tipologia,
                        marchio, modello, prodotto, modelloClass, codiceProdotto, costoProdotto,
                        costoCapitolato, nettoUsProdotto ){

    numeroPreventivo = numeroPreventivoParametro;
    dataPreventivo = dataPreventivoParametro;

    if( !$button.hasClass('aggiunto') ){


        //Segno nel bottono cliccato che e' una lavorazione aggiunto
        $button.addClass("aggiunto");
        $button.addClass("aggiunto-"+ordineProdotti);

        /*estraggo gli "id locali" della tipologia, del marchio e del modello */

        var splitModelloClass = modelloClass.split('_');
        var idTipologia = splitModelloClass[0].split('-')[1];
        var idMarchio = splitModelloClass[1].split('-')[1];
        var idModello = splitModelloClass[2].split('-')[1];
        var idTipMarcMod = idTipologia+"_"+idMarchio+"_"+idModello;

        /*memorizzo nel apposita sezione l'aggiunta della classe "aggiunto-"+ordineProdotti al bottone*/
        $("#memoriaProdottiAggiunti-"+idTipologia ).append(
            '<div class="'+$button.attr('id')+'">'+
                '<span class="classeToAdd">aggiunto-'+ordineProdotti+'</span>'+
            '</div>'

        );


        var tipologiaProdotto =  $('#bodyPreventivo').children('.tipologia-'+idTipologia);

        var diffCapitolato = Math.abs(  costoCapitolato-costoProdotto )
        var diffCapitolatoNum = diffCapitolato

        if( diffCapitolato == 0 ){
            diffCapitolato = '-';
        }
        else
            diffCapitolato = '&euro; '+diffCapitolato;

        //Preparo la riga del prodotto
        var rowsToAdd='<tr id="tipologia-'+idTipologia+'_trBody-'+ordineProdotti+'" class="trBody tipologia-'+idTipologia+'_lastAdded">'+
                        '<td class="firstCol'+ordineProdotti+' firstCol">'+
                            '<label></label><br/>'+
                            '<a onclick="cancellaProdotto($(this))" class="delElement fa fa-trash"></a>'+
                        '</td>'+
                        '<td class="tdPreventivo tdProdotto"><textarea>'+prodotto+'</textarea></td>'+
                        '<td class="tdPreventivo tdModello">'+modello+'</td>'+
                        '<td class="tdPreventivo tdCodice">'+codiceProdotto+'</td>'+
                        '<td class="tdPreventivo numColSmall tdQuantita"><input oninput="modificaQuantitaProdotto($(this), '+diffCapitolato+')" class="numInput numero" type="number" name="numero" placeholder="quantità" step="0.01" value="1.0"></td>'+
                        '<td class="tdPreventivo numColSmall"><input name="unitaMisura" placeholder="unita misura" value="cad"></td>'+
                        '<td class="tdPreventivo numColSmall tdDiffCapitolato">'+diffCapitolato+'</td>'+
                        '<td class="tdPreventivo tdAdded">&euro; '+ costoProdotto  +'</td>'+
                        '<td class="tdPreventivo tdAdded">&euro; '+ nettoUsProdotto +'</td>'+
                    '</tr>';

        //se non e' gia' stata aggiunta una sezione lo faccio e subito sotto metto il prodotto
        if( !tipologiaProdotto.length ){

            $('#bodyPreventivo').append(

                '<tr class="trHead tipologia-'+idTipologia'">'+
                    '<td  colspan="7"  class="titleTipologiaTd">'+tipologia+'</td>'+
                '</tr>'+
                '<tr class="trHead tipologia-'+idTipologia+'_head intestazione_head">'+
                    '<th class="thPreventivo"></th>'+
                    '<th class="thPreventivo">Nome prodotto</th>'+
                    '<th class="thPreventivo">Modello</th>'+
                    '<th class="thPreventivo">Codice</th>'+
                    '<th class="thPreventivo numColSmall">Quantità</th>'+
                    '<th class="thPreventivo numColSmall">Unità <br/> misura</th>'+
                    '<th class="thPreventivo">diff. CAPITOLATO</th>'+
                    '<th class="thPreventivo thAdded">Prezzo Listino</th>'+
                    '<th class="thPreventivo thAdded">Prezzo US</th>'+
                '</tr>'+
                rowsToAdd

            );
            $('.thAdded').hide();
            $('.tdAdded').hide();
        }
        else{

            var ultimoProdottoInserito=$(".tipologia-"+idTipologia+"_lastAdded");

            ultimoProdottoInserito.removeClass("tipologia-"+idTipologia+"_lastAdded");

            ultimoProdottoInserito.after( rowsToAdd );
            $('.tdAdded').hide();
        }

        $('tr.trBody').draggable({ helper: "clone"});


        /*registro la riga nel database*/
        socketFiniture.emit("add_nuovo_prodotto",
            {
                "numero_preventivo" : numeroPreventivo,
                "data" : dataPreventivo,
                "ordine": ordineProdotti,
                "tipologia" : tipologia,
                "prodotto" : prodotto,
                "modello" : modello,
                "marchio": marchio,
                "codice" : codiceProdotto,
                "quantita": 1,
                "unitaMisura": 'cad',
                "diffCapitolato": diffCapitolatoNum

            }

        );

        /*ad ogni nuova aggiunta di elemento rinumera tuttoquanto*/
        rienumeraPagina();

        calcolaTotalePreventivo();
        ordineProdotti++;


    }
}


/*****************************************************************************************************/

var suddividiProdottiPerModello = function(listaProdottiPerMarchio, listaModelliDistinti){

    /*
        Input:
        - listaProdottiPerMarchio = [ [nome_tipologia, [[nome_marchio, [[nome_modello, nome_prodotto],...]],...] ], ... ]
        - listaModelliDistinti = [nome_modello]

        Output:

        - marchiPerTipologia = [ [ nome_tipologia, [[nome_marchio, [[nome_modello, [nome_prodotto]],...]],...] ], ... ]

    */

    var marchiPerTipologia = [];

    // per ogni tipologia
    listaProdottiPerMarchio.forEach(function(tipologia){

        var modelliPerMarchio = [];


        // per ogni marchio
        tipologia[1].forEach(function(marchio){

            var prodottiPerModello = [];

            listaModelliDistinti.forEach(function(modello){

                var listProdotti = [];
                var modelloToAdd = false;

                //per ogni prodotto
                marchio[1].forEach(function(prodotto){

                    if( prodotto[0] == modello ){
                        modelloToAdd = true;
                        listProdotti.push(prodotto[1])
                    }

                });

                if(modelloToAdd)
                    prodottiPerModello.push([modello, listProdotti])

            });


            modelliPerMarchio.push([marchio[0], prodottiPerModello]);

        });

        marchiPerTipologia.push([tipologia[0], modelliPerMarchio]);

    });

    return marchiPerTipologia;


}
/****************************************************************************************************/

var suddividiProdottiPerMarchio = function(listaProdottiPerTipologia, listaMarchiDistinti){

    /*
        Input:
        - listaProdottiPerTipologia = [ [nome_tipologia, [[nome_marchio, nome_modello, nome_prodotto], ...]], ...]
        - listaMarchiDistiniti = [ nome_marchio ]

        Output:

        - marchiPerTipologia = [ [nome_tipologia, [[nome_marchio, [[nome_modello, nome_prodotto],...]],...] ], ... ]


    */

    var marchiPerTipologia = [];

    listaProdottiPerTipologia.forEach(function(tipologia){

        var prodottiPerMarchio = [];

        listaMarchiDistinti.forEach(function(marchio){

            var listProdotti = [];
            var marchioToAdd = false;

            tipologia[1].forEach(function(prodotto){


                if(prodotto[0] == marchio){

                    marchioToAdd = true;
                    listProdotti.push([ prodotto[1], prodotto[2] ]);
                }
            });

            if(marchioToAdd)
                prodottiPerMarchio.push([marchio, listProdotti])

        });


        marchiPerTipologia.push([tipologia[0], prodottiPerMarchio]);

    });


    return marchiPerTipologia;

}

/*************************************************************************/

var suddividiProdottiPerTipologiaMarchioModello = function(listaProdottiPerTipologia, listaMarchiDistinti, listaModelliDistinti){

    var prodottiPerTipologiaMarchio = suddividiProdottiPerMarchio( listaProdottiPerTipologia, listaMarchiDistinti );


    var prodottiSuddivisi = suddividiProdottiPerModello( prodottiPerTipologiaMarchio, listaModelliDistinti )


    return prodottiSuddivisi;

}

/*************************************************************************/

var aggiungiProdottiToSelectElement = function( listaProdottiPerTipologia, listaMarchiDistinti, listaModelliDistinti){

    var prodottiPerTipologiaMarchioModello = suddividiProdottiPerTipologiaMarchioModello( listaProdottiPerTipologia, listaMarchiDistinti, listaModelliDistinti );

    var counterTipologia = 0;
    prodottiPerTipologiaMarchioModello.forEach(function(tipologia){

        $('#selectTipologia').append('<option class="tipologia-'+counterTipologia+'">'+tipologia[0]+'</option>');

        var counterMarchio = 0;
        tipologia[1].forEach(function(marchio){

            $('#selectMarchio').append('<option class="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'">'+marchio[0]+'</option>');

            var counterModello = 0;
            marchio[1].forEach(function(modello){

                $('#selectModello').append('<option class="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'_modello-'+counterModello+'">'+modello[0]+'</option>');

                $('#memoriaProdottiAggiunti').append(
                     '<div id="memoriaProdottiAggiunti-'+counterTipologia+'" class="tipologiaMemorizzata"></div>'
                );

                var counterProdotto = 0;
                modello[1].forEach(function(prodotto){

                    $('#listaElementPreventivo').append(
                         '<li><button id="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'_modello-'+counterModello+'_prodotto-'+counterProdotto+'" class="elementFattura">'+
                         '<label for="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'_modello-'+counterModello+'_prodotto-'+counterProdotto+'">'+prodotto+'</label></button></li>'
                    );

                    counterProdotto++;
                });

                counterModello++;
            });

            counterMarchio++;
        });

        counterTipologia++;

    });

}

/***********************************************************************/
var showMarchiPerTipologia = function(tipologiaClass){

    $('#selectMarchio').children('option').hide();

    $('#selectMarchio').children('option').each(function(){

        if( $(this).attr('class').startsWith(tipologiaClass) ){

            $(this).show();

        }

    });

}

/************************************************************************/

var showModelliPerMarchio = function(marchioClass){

    $('#selectModello').children('option').hide();

    $('#selectModello').children('option').each(function(){

        if( $(this).attr('class').startsWith(marchioClass) ){

            $(this).show();

        }

    });

}

/************************************************************************/

var showProdottiPerModello = function(modelloClass){

    $('button.elementFattura').parent().hide();

    $('button.elementFattura').each(function(){

        if( $(this).attr('id').startsWith(modelloClass) ){

            $(this).parent().show();

        }

    });

}

/***************************************************************************/
/* Quando nascondo le opzioni in un select il valore del select non cambia e questo
    porta alla possibilità che come valore del select ne rimanga uno che debba
    sparire. Questa funzione reimposta il valore del select alla prima opzione
    non nascosta */

var impostaSelectedOptionVisibile = function($select){

    var firstOption = true;

    $select.children('option').each(function(){

        if( firstOption ){

            if( $(this).css('display') != 'none' ){
                $(this).attr('selected', 'selected')
                $select.trigger('change');
                firstOption = false;
            }
        }


    });
}
/**************************************************************************/


$(function(){

    $('#selectTipologia option:selected').each(function(){
        showMarchiPerTipologia($(this).attr('class'));
    });

    $('#selectMarchio option:selected').each(function(){
        showModelliPerMarchio($(this).attr('class'));
    });

    $('#selectModello option:selected').each(function(){
        showProdottiPerModello($(this).attr('class'));
    });

    $('#selectTipologia').change(function(){

        $(this).children('option:selected').each(function(){
            showMarchiPerTipologia($(this).attr('class'));
        });

        impostaSelectedOptionVisibile($('#selectMarchio'));

    });

    $('#selectMarchio').change(function(){

        $(this).children('option:selected').each(function(){
            showModelliPerMarchio($(this).attr('class'));
        });

        impostaSelectedOptionVisibile($('#selectModello'));

    });

    $('#selectModello').change(function(){

        $(this).children('option:selected').each(function(){
            showProdottiPerModello($(this).attr('class'));
        });

    });

});

/**************************************************************************/