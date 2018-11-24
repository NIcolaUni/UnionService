
var ordineProdotti = 1; // variabile globale usata per tener conto del numero dell'ultimo prodotto aggiunto


/********************************************************************************************/
function aggiungiRiga($button, numeroPreventivoParametro, dataPreventivoParametro, tipologia,
                        marchio, modello, prodotto, modelloClass, costoProdotto, costoCapitolato ){

    if( !$button.hasClass('aggiunto') ){


        //Segno nel bottono cliccato che e' una lavorazione aggiunto
        $button.addClass("aggiunto");
        $button.addClass("aggiunto-"+ordineProdotti);

        /*estraggo gli "id locali" della tipologia, del marchio e del modello */

        var splitModelloClass = modelloClass.split('_');
        var idTipologia = splitModelloClass[0].split('-')[1];
        var idMarchio = splitModelloClass[1].split('-')[1];
        var idModello = splitModelloClass[2].split('-')[1];

        /*memorizzo nel apposita sezione l'aggiunta della classe "aggiunto-"+ordineProdotti al bottone*/
        $("#memoriaProdottiAggiunti-"+idTipologia+"_"+idMarchio+"_"+idModello).append(
            '<div class="'+$button.attr('id')+'">'+
                '<span class="classeToAdd">aggiunto-'+ordineProdotti+'</span>'+
            '</div>'

        );


        var tipologiaProdotto =  $('#bodyPreventivo').children('.{{prodotto.tipologia}}');

        var diffCapitolato = Math.abs( parseFloat('{{capitolato.prezzoListinoFornituraPosa}}') - parseFloat('{{modello.prezzoListinoFornituraPosa}}') )
        var diffCapitolatoNum = diffCapitolato

        if( diffCapitolato == 0 ){
            diffCapitolato = '-';
        }
        else
            diffCapitolato = '&euro; '+diffCapitolato;

        //Preparo la riga del prodotto
        var rowsToAdd='<tr id="{{modello.tipologia}}_trBody-'+ordineProdotti+'" class="trBody {{modello.tipologia}}_lastAdded">'+
                        '<td class="firstCol'+ordineProdotti+' firstCol"></td>'+
                        '<td class="tdPreventivo tdProdotto"><textarea>{{modello.prodotto}}</textarea></td>'+
                        '<td class="tdPreventivo tdModello">{{modello.nome}}</td>'+
                        '<td class="tdPreventivo tdCodice">{{modello.codice}}</td>'+
                        '<td class="tdPreventivo numColSmall tdQuantita"><input class="numInput numero" type="number" name="numero" placeholder="quantità" step="0.01" value="1.0"></td>'+
                        '<td class="tdPreventivo numColSmall"><input name="unitaMisura" placeholder="unita misura" value="cad"></td>'+
                        '<td class="tdPreventivo numColSmall tdDiffCapitolato">'+diffCapitolato+'</td>'+
                        '<td class="tdPreventivo tdAdded">&euro; {{modello.prezzoListinoFornituraPosa}}</td>'+
                        '<td class="tdPreventivo tdAdded">&euro; {{modello.nettoUsFornituraPosa}}</td>'+
                    '</tr>';

        //se non e' gia' stata aggiunta una sezione lo faccio e subito sotto metto il prodotto
        if( !tipologiaProdotto.length ){

            $('#bodyPreventivo').append(

                '<tr class="trHead {{modello.tipologia}}">'+
                    '<td  colspan="7"  class="titleTipologiaTd">{{modello.tipologia}}</td>'+
                '</tr>'+
                '<tr class="trHead {{modello.tipologia}}_head intestazione_head">'+
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

            var ultimoProdottoInserito=$(".{{modello.tipologia}}_lastAdded");

            ultimoProdottoInserito.removeClass("{{modello.tipologia}}_lastAdded");

            ultimoProdottoInserito.after( rowsToAdd );
            $('.tdAdded').hide();
        }

        $('tr.trBody').draggable({ helper: "clone"});


        /*registro la riga nel database*/
        socketFiniture.emit("add_nuovo_prodotto",
            {
                "numero_preventivo" : "{{preventivo.numero_preventivo}}",
                "data" : "{{preventivo.data}}",
                "ordine": ordineProdotti,
                "tipologia" : "{{modello.tipologia}}",
                "prodotto" : "{{modello.prodotto}}",
                "modello" : "{{modello.nome}}",
                "marchio": "{{modello.marchio}}",
                "codice" : "{{modello.codice}}",
                "quantita": 1,
                "unitaMisura": 'cad',
                "diffCapitolato": diffCapitolatoNum

            }

        );

        /*ad ogni nuova aggiunta di elemento rinumera tuttoquanto*/
        rienumeraPagina();


        //Aggiungo funzionalita' ai "bottoni" nelle righe del preventivo e i bottoni stessi...
        $('.trBody').each(function(){

          var numEl = $(this).attr('id').split('-')[1];

          var diffCap = $(this).children('td.tdDiffCapitolato').html();

          if( diffCap != '-' )
            diffCap=parseFloat(diffCap.split(' ')[1]);

          $(this).children('td.tdQuantita').children('input').change(function(){

                var numValue = parseFloat($(this).val());
                var newCap = 0;

                if( diffCap != '-' )
                {
                    newCap = Math.round(diffCap*numValue*100)/100;

                    if( newCap == 0 )
                        $(this).parent().parent().children('td.tdDiffCapitolato').html('-');
                    else
                        $(this).parent().parent().children('td.tdDiffCapitolato').html('&euro; '+newCap);

                }

                calcolaTotalePreventivo();

                socketFiniture.emit("modifica_prodotto",
                                {
                                    "numero_preventivo" : "{{preventivo.numero_preventivo}}",
                                    "data" : "{{preventivo.data}}",
                                    "ordine": numEl,
                                    "quantita": numValue,
                                    "diffCapitolato": newCap

                                }
                );

          });

          //aggiungo il bottoni di cancellazioni e il numero elemento
          $(this).children('td.firstCol').html( '<label>'+ numEl + '</label><br/><a class="delElement fa fa-trash"></a>' );


          //aggiungo la funzione 'cancellaLavorazione' al relativo bottone
          $(this).children('td.firstCol').children('a.delElement').click(function(){
                var idElementToDel=$(this).parent().parent().attr('id');
                var numEl = idElementToDel.split('-')[1];
                var tipologia =idElementToDel.split('_')[0];
                var lastEl = $('#'+idElementToDel).hasClass(tipologia+'_lastAdded'); //variabile booleana


                $('#'+idElementToDel).remove();

                $('#memoriaProdottiAggiunti-'+tipologia).children('div').each(function(){
                    if( $(this).text() == 'aggiunto-'+numEl )
                        $(this).remove();
                });

                $('.aggiunto-'+numEl).removeClass('aggiunto');
                $('.aggiunto-'+numEl).removeClass('aggiunto-'+numEl);

                socketFiniture.emit("elimina_prodotto",
                                {
                                    "numero_preventivo" : "{{preventivo.numero_preventivo}}",
                                    "data" : "{{preventivo.data}}",
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

                    $('.'+tipologia).each(function(){
                        if($(this).hasClass('trHead'))
                            $(this).remove();
                    });

                    $('.'+tipologia+'_head').remove();

                }
          });

        });

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
                     '<div id="memoriaProdottiAggiunti-'+counterTipologia+'_'+counterMarchio+'_'+counterModello+'" class="tipologiaMemorizzata"></div>'
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