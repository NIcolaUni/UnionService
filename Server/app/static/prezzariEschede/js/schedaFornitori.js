var filterZoneOpenWidthPerc = 70;
var firstTime = 0; //usata per compiere operazioni solo all'apertura della pagina
/******************************************************************************************************/
var eventoCambiaTabella = function(){
    $('.newPageCell a').click(function(){
        $('#tabellaContainer3').show();
        $('#headerTableContainer_3').show();
        $('#tabellaContainer2').css('left', 'unset');
        $('#headerTableContainer_2').css('left', 'unset');
       // $('#tabellaContainer2').animate({"right": $('#tabellaContainer2').width()+2});
        $('#tabellaContainer3').animate({"left": $('#tabellaContainer1').width()+2});
        $('#headerTableContainer_3').animate({"left": $('#headerTableContainer_1').width()+2});
        $('#tabellaContainer2').css('display', 'none');
        $('#headerTableContainer_2').css('display', 'none');
    });

    $('.oldPageCell a').click(function(){

        $('#tabellaContainer2').show();
        $('#headerTableContainer_2').show();

        $('#tabellaContainer2').animate({"left": $('#tabellaContainer1').width()+2});
        $('#headerTableContainer_2').animate({"left": $('#tabellaContainer1').width()+2});
        $('#tabellaContainer3').animate({"left": $('#tabellaContainer1').width()+2+$('#tabellaContainer2').width()});
        $('#headerTableContainer_3').animate({"left": $('#tabellaContainer1').width()+2+$('#tabellaContainer2').width()});
        $('#tabellaContainer3').css('display', 'none');
        $('#headerTableContainer_3').css('display', 'none');

    });

    $('.newPageCell.newRow a').unbind().click(function(){
        $('#tabellaContainerNewRow3').show();
        $('#tabellaContainerNewRow2').animate({"left": '-=46%'});
        $('#tabellaContainerNewRow3').animate({"left": '-=46%'});
    });

    $('.oldPageCell.newRow a').unbind().click(function(){
        $('#tabellaContainerNewRow2').animate({"left": '+=46%'});
        $('#tabellaContainerNewRow3').animate({"left": '+=46%'}, function(){$('#tabellaContainerNewRow3').hide()});

    });
}
/******************************************************************************************************/

var pulisciHeaderNewRow = function(){
    //ripulisco i vari campi del aggiungi riga
    var firstRadio=true;
    $('#headerNewRow input').each(function(){
        if( $(this).attr('type') == 'radio' ){

            if( firstRadio ){
                $(this).trigger('click')
                firstRadio=false;
            }
            else{
                firstRadio=true;

            }
        }
        else if( $(this).attr('type') == 'number' )
            $(this).val('0');
        else
            $(this).val('');
    });

}

/********************************************************************************************/

var higherRowHeight = function( containerId, sezioneClass ){

    var result = 0;

    for( var i = 1; i <4; i++ ){
        $('#'+ containerId+ i +' .'+sezioneClass).each(function(){
            if($(this).height() > result){
                result = $(this).height();
            }
        });
    }

    return result;
}

/********************************************************************************************/

var setRowHeight = function(height, containerId, sezioneClass){

    for( var i = 1; i <4; i++ ){
        $('#'+containerId+ i +' .'+sezioneClass).each(function(){
            $(this).height(height);
        });
    }

}


/********************************************************************************************/

var equalizzaAltezzaAggiungiFornitore = function(){

    setRowHeight(higherRowHeight('tabellaContainerNewRow', 'datiScheda'), 'tabellaContainerNewRow', 'datiScheda');
    setRowHeight(higherRowHeight('tabellaContainerNewRow', 'headerTabella'), 'tabellaContainerNewRow', 'headerTabella');


}


/******************************************************************************************/

var equalizzaAltezzaRighe = function(){


    setRowHeight(higherRowHeight('tabellaContainer', 'datiScheda'), 'tabellaContainer', 'datiScheda');

}

/******************************************************************************************/

var equalizzaAltezzaHeader = function(){

    setRowHeight(higherRowHeight('headerTableContainer_', 'headerTabella'), 'headerTableContainer_', 'headerTabella');

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

        var diffOffsetContainerTabella = leftOffsetTabella-$('')//-leftOffesetHeaderContainer;

        $header.css('left', diffOffsetContainerTabella+'px')


    }
    else if( numHeader == 2 ){

        var diffOffsetContainerTabella = leftOffsetTabella-leftOffesetHeaderContainer;

        $header.css('left', diffOffsetContainerTabella+'px')


    }
    else if( numHeader == 3 ){

        var spostamento =  $('#headerTableContainer_2').offset().left+$('#headerTableContainer_2').width()-$('.viewContainer').offset().left;
      //  alert('spos ' + spostamento)
        $header.css('left', spostamento)
        $header.css('display', 'none')

    }

     firstTime++;
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

/******************************************************************************************/


var posizionaTabellaFornitori = function(){

    if( firstTime < 1 ){
        $('#tabellaContainer2').css('left', $('#tabellaContainer1').width()+2);
        $('#tabellaContainer3').css('left', $('#tabellaContainer1').width()+2+$('#tabellaContainer2').width());

    }
    //$('.filterZoneScheda').css('right', $('.filterZoneScheda').width()*(2/3));
}

/*********************************************************************************/

var primaColSize = '5%'
var tabellaSize = $(window).height()*65/100;

var dimensioniCellePrimaTabella = function($cella){
    if( $cella.hasClass('primaCol') ){
        $cella.css('width', primaColSize)
    }
    else if( $cella.hasClass('long_string') ){
        $cella.css('width', '45%')

    }
    else if( $cella.hasClass('normal_string') ){
        $cella.css('width', '25%')
    }

    equalizzaAltezzaRighe();
}

var dimensioniCelleSecondaTabella = function($cella){

    if( $cella.hasClass('normal_string')){
        $cella.css('width', '40%');
    }
    else if( $cella.hasClass('numCell')){
        $cella.css('width', '15%');
    }

}

var dimensioniCelleTerzaTabella = function($cella){


    if( $cella.hasClass('normal_string')){
        $cella.css('width', '23%');
    }
    else if( $cella.hasClass('numCell')){
        $cella.css('width', '10%');
    }

}

var regolaDimensioniHeader = function(idHeaderContainer, idTabellaContainer){

    posizionaTabellaFornitori();

    $('.viewContainer').css( {height: tabellaSize+'px'});

    allineaVerticalmenteHeader( $('#'+idHeaderContainer) );

    if( firstTime < 3)
        allineaOrizzontalmenteHeader( $('#'+idHeaderContainer), $('#'+idTabellaContainer) );


    $('#'+idHeaderContainer).width( $('#'+idTabellaContainer).width() );

    var numberTable = parseInt(idHeaderContainer.split('_')[1]);

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
                else if(numberTable == 3 ){
                    dimensioniCelleTerzaTabella($(this))
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
                    else if(numberTable == 3 ){
                        dimensioniCelleTerzaTabella($(this))
                    }
                 }

            });
        }
    });


}
/**********************************************************************************************/

$(function(){
    eventoCambiaTabella();
});