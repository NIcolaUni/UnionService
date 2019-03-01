
var disabilitaSocketIo = false;
var numero_preventivo;
var revisione;
var listaArtigiani = []; //impostata all'apertura della pagina per poter poi creare i selectArtiagino
                         // degli imprevesti a runtime
/*********************************************************************************************/

var settaVariabiliSocketIo = function(numero_prev, rev){
    numero_preventivo=numero_prev;
    revisione=rev;

}

/***********************************************************************************************/

var settaDisabilitaSocketIo = function(val){
    disabilitaSocketIo = val;
}

/**********************************************************************************************/

var impostaListaArtigiani = function(list){
    listaArtigiani = list
}

/*********************************************************************************************/
var settaTotaleContabilita= function(){

    var $tabellaEdile = $('table.edile tbody');
    //var $tabellaBudget = $('table.budget_imprevisti tbody');

    var totaleBudgetTabellaEdile = 0
    var totaleCostiEffTabellaEdile = 0
    var totaleFattureTabellaEdile = 0



    //faccio le somme delle colonne budget, costi effettivi, fatture della tabella .edile
    $tabellaEdile.children('tr.trBody').each(function(){

       var num = $(this).children('td.tdBudget').text().split(' ')[1];


       if(num == '')
            num = 0


       totaleBudgetTabellaEdile += parseFloat(num);

       var num = $(this).children('td.tdCostiEffettivi').children('input').val();


       if(num == '')
            num = 0

       totaleCostiEffTabellaEdile += parseFloat(num);

       var num = $(this).children('td.tdFatture').children('input').val();


       if(num == '')
            num = 0

       totaleFattureTabellaEdile += parseFloat(num);


    });

    var budget_imprevisti = parseFloat($('.trBody.budget_imprevisti').children('td.tdBudget').text().split(' ')[1]);

    var totaleBudget =totaleBudgetTabellaEdile + budget_imprevisti;
    totaleBudget = Math.round(totaleBudget*100)/100;

    $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotBudget').html('&euro; '+totaleBudget);

    var costo_imprevisti = 0;

    $('#bodyTabellaBudget').children('tr.imprevisti').each(function(){

        costo_imprevisti += parseFloat($(this).children('td.tdCostiEffettivi').children('input').val());
    });

    var totaleCostiEff = totaleCostiEffTabellaEdile + costo_imprevisti;
    totaleCostiEff = Math.round(totaleCostiEff*100)/100;

    var diff_budget_e_imprevisti =  costo_imprevisti-budget_imprevisti;

    diff_budget_e_imprevisti = Math.round( diff_budget_e_imprevisti*100 )/100;

    if( diff_budget_e_imprevisti > 0 )
    {
        $('.trBody.budget_imprevisti').children('td.tdControlloCosti').html('<label class="red">&euro; +'+diff_budget_e_imprevisti+'</label>');
    }
    else{
        $('.trBody.budget_imprevisti').children('td.tdControlloCosti').html('<label class="green">&euro; '+diff_budget_e_imprevisti+'</label>');
    }

    $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotCostiEffettivi').html('&euro; '+totaleCostiEff);

    var diff_totali =  totaleCostiEff -totaleBudget;
    diff_totali = Math.round( diff_totali*100 )/100;

    if( diff_totali > 0 ){
        $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotControlloCosti').html('<label class="red">&euro; +'+diff_totali+'</label>');
    }
    else{
        $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotControlloCosti').html('<label class="green">&euro; '+diff_totali+'</label>');
    }


    var fatture_imprevisti = 0;

    $('#bodyTabellaBudget').children('tr.imprevisti').each(function(){

        fatture_imprevisti += parseFloat($(this).children('td.tdFatture').children('input').val());
    });

    var sommaFatture = totaleFattureTabellaEdile+fatture_imprevisti;
    sommaFatture = Math.round(sommaFatture*100)/100;

    $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotFatture').html('&euro; '+sommaFatture);


    var diff_costo_fatture = sommaFatture - totaleCostiEff

    diff_costo_fatture = Math.round( diff_costo_fatture*100 )/100;

    if( diff_costo_fatture > 0 ){
        $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotControlloFatture').html('<label class="red">&euro; +'+diff_costo_fatture+'</label>');
    }
    else{
        $('#bodyTabellaResult tr.trBody.totale').children('td.tdTotControlloFatture').html('<label class="green">&euro; '+diff_costo_fatture+'</label>');
    }

    var prezzoContratto = parseFloat($('tr.trBody.prezzoClienteContratto').children('td.prezzoContratto').html().split(' ')[1]);
    var utile_netto_costi_eff = prezzoContratto - totaleCostiEff;

    utile_netto_costi_eff = Math.round(utile_netto_costi_eff*100)/100;

    var abs_utile_netto = Math.abs(utile_netto_costi_eff);

    var utile_costi_eff_percentuale = abs_utile_netto*100/prezzoContratto;

    utile_costi_eff_percentuale = Math.round(utile_costi_eff_percentuale*100)/100;


    if( utile_netto_costi_eff > 0 ){
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_netto_costi_eff').html('<label class="green">&euro; '+utile_netto_costi_eff+'</label>');
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_perc_costi_eff').html('<label class="green">'+utile_costi_eff_percentuale+' %</label>');
    }
    else{
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_netto_costi_eff').html('<label class="red">&euro; '+utile_netto_costi_eff+'</label>');
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_perc_costi_eff').html('<label class="red">-'+utile_costi_eff_percentuale+' %</label>');
    }


    var utile_netto_fatture = prezzoContratto - sommaFatture;

    utile_netto_fatture = Math.round(utile_netto_fatture*100)/100;

    abs_utile_netto = Math.abs(utile_netto_fatture);

    var utile_fatture_percentuale= abs_utile_netto*100/prezzoContratto;

    utile_fatture_percentuale = Math.round(utile_fatture_percentuale*100)/100;


    if( utile_netto_fatture > 0 ){
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_netto_fatture').html('<label class="green">&euro; '+utile_netto_fatture+'</label>');
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_perc_fatture').html('<label class="green">'+utile_fatture_percentuale+' %</label>');
    }
    else{
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_netto_fatture').html('<label class="red">&euro; '+utile_netto_fatture+'</label>');
        $('#bodyTabellaResult tr.trBody.utile').children('td.utile_perc_fatture').html('<label class="red">-'+utile_fatture_percentuale+' %</label>');
    }


}

var rienumeraImprevisti = function(){
    var ordineUltimaLavorazionePreventivo = parseInt( $('table.edile tbody').children('tr.trBody').last().children('td').first().html() );

    $('.trBody.imprevisti').each(function(){
        var ordineToMod = parseInt($(this).children('td').first().children('label').text());

        $(this).children('td').first().children('label').text(-ordineToMod)

        if(!disabilitaSocketIo)
            socketContabilita.emit('modifica_imprevisto',{
                'numero_preventivo' : numero_preventivo,
                'revisione': revisione,
                'ordine': ordineToMod,
                'toMod': 'ordine',
                'val': -ordineToMod

            });

    });

    $('.trBody.imprevisti').each(function(){
        var ordineToMod = parseInt($(this).children('td').first().children('label').text());
        ordineUltimaLavorazionePreventivo++;
        $(this).children('td').first().children('label').text(ordineUltimaLavorazionePreventivo)

        if(!disabilitaSocketIo)
            socketContabilita.emit('modifica_imprevisto',{
                'numero_preventivo' : numero_preventivo,
                'revisione': revisione,
                'ordine': ordineToMod,
                'toMod': 'ordine',
                'val': ordineUltimaLavorazionePreventivo

            });

    });
}

var eliminaImprevisto = function($this){

    $this.parent().parent().remove();

    var ordineToDel = parseInt($this.parent().parent().children('td').first().children('label').text());


    if(!disabilitaSocketIo)
        socketContabilita.emit('elimina_imprevisto', {
            'numero_preventivo' : numero_preventivo,
            'revisione': revisione,
            'ordine': ordineToDel
        });

    rienumeraImprevisti();

}

var modificaNomeImprevisto = function($this){

    var ordineToMod = parseInt($this.parent().parent().children('td').first().children('label').text());

    if(!disabilitaSocketIo){

        socketContabilita.emit('modifica_imprevisto',{
            'numero_preventivo' : numero_preventivo,
            'revisione': revisione,
            'ordine': ordineToMod ,
            'toMod': 'nome',
            'val': $this.val().replace(/\n/g, "")

        });

    }

}

var modificaCostoImprevisto = function($this){


    var ordineToMod = parseInt($this.parent().parent().children('td').first().children('label').text());
    if(!disabilitaSocketIo)
        socketContabilita.emit('modifica_imprevisto',{
            'numero_preventivo' : numero_preventivo,
            'revisione': revisione,
            'ordine': ordineToMod,
            'toMod': 'costo',
            'val': $this.val()

        });

    settaTotaleContabilita()

}

var modificaCostoFatturaImprevisto = function($this){

    var ordineToMod = parseInt($this.parent().parent().children('td').first().children('label').text());
    if(!disabilitaSocketIo)
        socketContabilita.emit('modifica_imprevisto',{
            'numero_preventivo' : numero_preventivo,
            'revisione': revisione,
            'ordine': ordineToMod,
            'toMod': 'costo_fattura',
            'val': $this.val()

        });

    settaTotaleContabilita()
}

var modificaArtigianoLavorazione = function($this){

    alert('ndsjsjksjk')
    var $riga = $this.parent().parent();
    var selectedChoiceArray = $this.val().split(' - ');
    var nome_artigiano = selectedChoiceArray[0];
    var impiego_artigiano = selectedChoiceArray[1];
    var ordine_lav = 0;

    var tipologia = $riga.parent().children('tr.titleTable').children().text();

    if(tipologia == 'Preventivo Edile'){
        tipologia = 'edile';
        ordine_lav = parseInt($riga.children('td.tdOrdineLav').text());
    }
    else if( tipologia == 'Budget Imprevisti'){
        tipologia='imprevisti';
        ordine_lav = parseInt($riga.children('td.tdOrdineImprevisto').children('label.ordineImprevisto').text())
    }

    if(!disabilitaSocketIo)
        socketContabilita.emit('modifica_artigiano_contabilita',{
            'numero_preventivo' : numero_preventivo,
            'revisione': revisione,
            'ordine_lav': ordine_lav,
            'tipologia': tipologia,
            'nome_artigiano': nome_artigiano,
            'impiego_artigiano': impiego_artigiano

        });

}


/**********************************************************************************************/
$(function(){

    $('.inputNumber.effettuaControllo').on('input', function(){
        var $cella =$(this).parent();
        var $riga = $cella.parent();
        var valoreInput = $(this).val()

        if( $cella.hasClass('tdCostiEffettivi') ){

            var valoreBudget = parseFloat($riga.children('td.tdBudget').text().split(' ')[1]);

            var differenza = valoreInput-valoreBudget;
            var colorClass;

            if( differenza > 0 ){

               colorClass = 'red';
               $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'">&euro; +'+ Math.abs(Math.round(differenza*100)/100)+'</label>' );

            }
            else if( differenza < 0 ){

                colorClass = 'green';
                $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'">&euro; -'+ Math.abs(Math.round(differenza*100)/100)+'</label>' );
            }
            else{
                colorClass = 'green';
                $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'"> &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );
            }


            if( !disabilitaSocketIo )
                //VAnno modificati tipologia_lavorazione e ordine ( il primo e' da trasformare in tipologia )

                var toModVal = 'costi_effettivi';

                if($riga.parent().parent().attr('class').split(' ')[1] == 'budget_imprevisti' ){

                    toModVal = 'costi_effettivi_budget_imprevisti';
                    //$('#bodyTabellaResult tr.trBody.budgetNonUsato').children('td.tdControlloCosti').html('<label class="'+colorClass+'"> + &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>');

                }

                if(!disabilitaSocketIo)
                    socketContabilita.emit('modifica_contabilita',
                        {
                            'numero_preventivo': numero_preventivo,
                            'revisione': revisione,
                            'tipologia': $riga.parent().parent().attr('class').split(' ')[1],
                            'ordine': $riga.children('td.tdOrdineLav').text(),
                            'toMod': toModVal,
                            'newVal': valoreInput

                        }
                    );

        }
        else if( $cella.hasClass('tdFatture') ){

            var valoreCostiEff = parseFloat($riga.children('td.tdCostiEffettivi').children('input').val());

            var differenza = valoreInput - valoreCostiEff;
            var colorClass;

            if( differenza > 0 ){
               colorClass = 'red';
               $riga.children('td.tdControlloFatture').html('<label class="'+colorClass+'">&euro; +'+ Math.abs(Math.round(differenza*100)/100)+'</label>' );


            }
            else if( differenza < 0 ){

                colorClass = 'green';
                $riga.children('td.tdControlloFatture').html('<label class="'+colorClass+'">&euro; -'+ Math.abs(Math.round(differenza*100)/100)+'</label>' );

            }
            else{
                colorClass = 'green';
                $riga.children('td.tdControlloFatture').html('<label class="'+colorClass+'"> &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );
            }


            if( !disabilitaSocketIo ){
                var toModVal = 'fattura';

                if($riga.parent().parent().attr('class').split(' ')[1] == 'budget_imprevisti' )
                    toModVal = 'fattura_budget_imprevisti';



                socketContabilita.emit('modifica_contabilita',
                    {
                        'numero_preventivo': numero_preventivo,
                        'revisione': revisione,
                        'tipologia': $riga.parent().parent().attr('class').split(' ')[1],
                        'toMod': toModVal,
                        'ordine': $riga.children('td.tdOrdineLav').text(),
                        'newVal': valoreInput

                    }
                );
            }

        }


    });

    $('.inputNumber.effettuaControllo').on('input', function(){
        settaTotaleContabilita();
    });

    settaDisabilitaSocketIo(true);
    $('.inputNumber.effettuaControllo').trigger('input');
    settaDisabilitaSocketIo(false);

    settaTotaleContabilita();

    $('#aggiungiImprevisti').click(function(){

        var ordine_imprevisto = 0;

        if( $('.trBody.imprevisti').length == 0 ){
            ordine_imprevisto = parseInt( $('table.edile tbody').children('tr.trBody').last().children('td').first().html() )+1;
        }
        else{
            ordine_imprevisto = parseInt( $('table.budget_imprevisti tbody').children('tr.trBody').last().children('td').first().children('label').html() )+1;
        }

        var optionsSelectArtigiani = '<option>no artigiano</option>';

        $.each(listaArtigiani, function(index, el){
            optionsSelectArtigiani += '<option>'+el+'</option>';
        });

        var $rowToInsert= '<tr class="trBody imprevisti"> \
                                    <td><label class="ordineImprevisto">'+ordine_imprevisto+'</label><a onclick="eliminaImprevisto($(this))" class="fa fa-trash eliminaImprevisto"></a></td> \
                                    <td class="tdNomeImprevisto"><textarea  oninput="modificaNomeImprevisto($(this))" class="nomeImprevisto"></textarea></td> \
                                    <td class="tdArtigiano"> \
                                        <select onchange="modificaArtigianoLavorazione($(this))" class="selectArtigiano">'+
                                        optionsSelectArtigiani+
                                        '</select> \
                                    </td> \
                                    <td></td> \
                                    <td class="tdCostiEffettivi">&euro; <input oninput="modificaCostoImprevisto($(this))" class="inputNumber costoImprevisto" type="number" min="0" value="0"> </td> \
                                    <td class="tdControlloCosti"></td> \
                                    <td class="tdFatture"> &euro; <input oninput="modificaCostoFatturaImprevisto($(this))" class="inputNumber fatturaImprevisto effettuaControllo" type="number" min="0" value="0"> </td> \
                                    <td class="tdControlloFatture"></td> \
                                </tr>'

        if( $('.trBody.imprevisti').length == 0 ){
            $('.trBody.budget_imprevisti').after($rowToInsert);
        }
        else{
            $('.trBody.imprevisti').last().after($rowToInsert);
        }

        if(!disabilitaSocketIo)
            socketContabilita.emit('registra_imprevisto', {
                'numero_preventivo' : numero_preventivo,
                'revisione': revisione,
                'ordine': ordine_imprevisto
            });



    });





});