var divAziendaAssente=true;
var filterZoneOpenWidthPerc = 60;

/******************************************************************************************/

/******************************************************************************************/

/******************************************************************************************/

/******************************************************************************************************/

var hiddenInputAction = function($this){

    $('.inModifica').each(function(){
        $(this).removeClass('inModifica');
        $(this).children('label').show();
        $(this).children('input').hide();
        //$(this).children('select').hide();
        $(this).children('.radioLabel').hide();
        $(this).children('.checked').show();
        $(this).children('.simpleAfterInputLabel').show();
        $(this).children('.unita').each(function(){
            $(this).hide();
        });

        $(this).children('.posa').each(function(){
            $(this).children('input.posa').hide();
            $(this).parent().children('span').children().each(function(){

                $(this).hide();
            });;
        });

    });


    $this.addClass('inModifica');
    $this.children('label').hide();
    $this.children('input').show();
   // $this.children('select').show();

    $this.children('.radioLabel').show();
    $this.children('.simpleAfterInputLabel').show();

    $this.children('.unita').each(function(){
            $(this).show();
    });

    $this.children('.posa').each(function(){

            $(this).children('input.posa').show();
            $(this).parent().children('span').children().each(function(){

                $(this).show();
            });;
    });


    if( !$this.children('input').hasClass('posa') )
        $this.children('input.inputScheda').focus();


}

/******************************************************************************************************/

var pulisciHeaderNewRow = function(){

    $('#headerNewRow input').each(function(){

        if( $('#setCapitolato').is(':checked') )
        {
            $('#setCapitolato').trigger('click');
        }


        if($(this).hasClass('numInput'))
            $(this).val(0);
        else if($(this).hasClass('posaPerc'))
            $(this).val(50);
        else
        {
            $(this).val('');

        }
    });


    if( $('#tabellaContainerNewRow2 .datiScheda').hasClass('azienda') ){
       $('#tabellaContainerNewRow2 .datiScheda').removeClass('azienda')


       var altezzaHeaderNewRow = $('#tabellaContainerNewRow2').height();
       var altezzaContainer3 = $('#tabellaContainerNewRow3').height();

       $('#tabellaContainerNewRow3').animate({'top': '-'+(altezzaHeaderNewRow-altezzaContainer3)+'px'});

       divAziendaAssente=true;
    }
    else if( $('#tabellaContainerNewRow2 .datiScheda').hasClass('fornitore') ){
       $('#tabellaContainerNewRow2 .datiScheda').removeClass('fornitore')

    }

}

/******************************************************************************************/

var prodottiInListaProdotti = function(prodotto){

    var toAdd = true;

    $('#listaProdotti').children('option').each(function(){
        if( $(this).val() == prodotto ){
            toAdd = false;
        }
    });

    if( toAdd ){
        $('#listaProdotti').append('<option>'+prodotto+'</option>');
    }
}

/********************************************************************************************/

var equalizzaAltezzaAggiungiProdotto = function(){


    /*trovo la riga più alta*/
    var tallerRow=0;

    $('#tabellaContainerNewRow1 .datiScheda').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#tabellaContainerNewRow2 .datiScheda').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#tabellaContainerNewRow1 .datiScheda').each(function(){
        $(this).height(tallerRow);

    });

    $('#tabellaContainerNewRow2 .datiScheda').each(function(){
        $(this).height(tallerRow);
    });

    tallerRow = 0;

    $('#tabellaContainerNewRow1 .headerTabella').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#tabellaContainerNewRow2 .headerTabella').each(function(){
        if($(this).height() > tallerRow){
            tallerRow = $(this).height();
        }
    });

    $('#tabellaContainerNewRow1 .headerTabella').each(function(){
        $(this).height(tallerRow);

    });

    $('#tabellaContainerNewRow2 .headerTabella').each(function(){
        $(this).height(tallerRow);
    });


}


/******************************************************************************************/

var equalizzaAltezzaRighe = function(){

    /*trovo la riga più alta*/
    var tallerRow=0;

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

        var diffOffsetContainerTabella = leftOffesetHeaderContainer-leftOffsetTabella;

        $header.css('margin-left', '-'+diffOffsetContainerTabella+'px')

    }
    else if( numHeader == 2 ){

        var diffOffsetContainerTabella = leftOffsetTabella-leftOffesetHeaderContainer;

        $header.css('left', diffOffsetContainerTabella+'px')


    }


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

/*******************************************************************************************/
/*
Per ogni prezzario o schedario, la dimensione delle celle della tabella e del suo header
vengoro regolati col codice seguente;
*/
var primaColSize = '10%'

var dimensioniCellePrimaTabella = function($cella){
    if( $cella.hasClass('primaCol') ){
        $cella.css('width', primaColSize)
    }
    else if( $cella.hasClass('long_string') ){
        $cella.css('width', '30%')

    }
    else if( $cella.hasClass('normal_string') ){
        $cella.css('width', '15%')
    }

    equalizzaAltezzaRighe();
}

var dimensioniCelleSecondaTabella = function($cella){

    $cella.css('width', '14%')

}


var tabellaSize = $(window).height()*65/100;

var regolaDimensioniHeader = function(idHeaderContainer, idTabellaContainer){

    $('.viewContainer').css( {height: tabellaSize+'px'});

    allineaVerticalmenteHeader( $('#'+idHeaderContainer) );
    allineaOrizzontalmenteHeader( $('#'+idHeaderContainer), $('#'+idTabellaContainer) );


    $('#'+idHeaderContainer).width( $('#'+idTabellaContainer).width() );

    var numberTable = parseInt(idHeaderContainer.split('_')[1]);


    //Per ogni cella dell'header mi assicuro che le dimensioni corrispondano con le
    //celle della tabella contenente i dati

    var indexElement =0;

    $('#'+idHeaderContainer+' tbody').children('tr').each(function(){

        if( $(this).hasClass('headerDelHeader') ){
        //    alert('qua: '+$(this).attr('class'))

            $('this').children('td.primaCol').css('width', primaColSize );
        }
        else{

            $('#'+idTabellaContainer+' .sezioneTabella').children('td.primaCol').css('width', primaColSize );
          //  alert($(this).attr('class'))
            $(this).children('th').each(function(){

                if(numberTable == 1 ){
                    dimensioniCellePrimaTabella($(this))
                }
                else if(numberTable == 2 ){
                    dimensioniCelleSecondaTabella($(this))
                }


            });

            $('#'+idTabellaContainer+' .datiScheda').children('td').each(function(){
                 if(!$(this).hasClass('tipologia')){

                    if(numberTable == 1 ){
                        dimensioniCellePrimaTabella($(this))
                    }
                    else if(numberTable == 2 ){
                        dimensioniCelleSecondaTabella($(this))
                    }

                 }

            });
        }
    });

    equalizzaAltezzaAggiungiProdotto();
}


/**************************************************************************************/

$(function(){

    setTimeout(function(){
        equalizzaAltezzaHeader();
        window.addEventListener('resize', equalizzaAltezzaHeader());
    }, 100);



});