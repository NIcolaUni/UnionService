
var disabilitaSocketIo = false;
var numero_preventivo;
var revisione;
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

$(function(){

    $('.inputNumber').on('input', function(){
        var $cella =$(this).parent();
        var $riga = $cella.parent();
        var valoreInput = $(this).val()

        if( $cella.hasClass('tdCostiEffettivi') ){

            var valoreBudget = parseFloat($riga.children('td.tdBudget').text().split(' ')[1]);

            var differenza = valoreInput-valoreBudget;
            var colorClass;

            if( differenza > 0 ){

               colorClass = 'red';
               $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'"> + &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );

            }
            else if( differenza < 0 ){

                colorClass = 'green';
                $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'"> - &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );

            }
            else{
                colorClass = 'green';
                $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'"> &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );

            }


            if( !disabilitaSocketIo )
                socketContabilita.emit('modifica_contabilita',
                    {
                        'numero_preventivo': numero_preventivo,
                        'revisione': revisione,
                        'tipologia_lavorazione': $riga.children('td.tdNomeLav').text(),
                        'toMod': 'costi_effettivi',
                        'newVal': valoreInput

                    }
                );

        }
        else{

            var valoreCostiEff = parseFloat($riga.children('td.tdCostiEffettivi').children('input').val());

            var differenza = valoreInput - valoreCostiEff;
            var colorClass;

            if( differenza > 0 ){
               colorClass = 'red';
               $riga.children('td.tdControlloFatture').html('<label class="'+colorClass+'"> + &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );


            }
            else if( differenza < 0 ){

                colorClass = 'green';
                $riga.children('td.tdControlloFatture').html('<label class="'+colorClass+'"> - &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );

            }
            else{
                colorClass = 'green';
                $riga.children('td.tdControlloCosti').html('<label class="'+colorClass+'"> &euro; '+ Math.abs(Math.round(differenza*100)/100)+'</label>' );
            }


            if( !disabilitaSocketIo )
                socketContabilita.emit('modifica_contabilita',
                    {
                        'numero_preventivo': numero_preventivo,
                        'revisione': revisione,
                        'tipologia_lavorazione': $riga.children('td.tdNomeLav').text(),
                        'toMod': 'fattura',
                        'newVal': valoreInput

                    }
                );

        }

    });

    settaDisabilitaSocketIo(true);
    $('.inputNumber').trigger('input');
    settaDisabilitaSocketIo(false);
});