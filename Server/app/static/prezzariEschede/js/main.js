

/*******************************************************************************************/

    var regolaDimensioniForEachHeader = function(){
        var countTables=1;

        $('.viewContainer').children('div').each(function(){

             regolaDimensioniHeader( 'headerTableContainer_'+countTables,$(this).attr('id'));
             countTables++;
        });

        riposizionaTabelle();

    }

/**********************************************************************************************/

$(function(){

/***************************************************************************/

var settaDimensioniIconaFilterZoneOpen = function(){

    var iconHeight = $(window).height()*25/100;
    var iconWidth =$(window).width()*filterZoneOpenWidthPerc/100;

    $('.filterZoneScheda.open').css('width', iconWidth+'px');
    $('.filterZoneScheda.open').css('height', iconHeight+'px');

    $('#openCloseFilterSearch').css('width', '8%');
    $('#openCloseFilterSearch').css('float', 'right');



    $('#openCloseFilterSearch').css('margin-right', '2%');
    $('#openCloseFilterSearch').css('margin-top', '1%');

    $('#openCloseFilterSearch a').css('font-size', '30px');

    if(filterZoneOpenWidthPerc > 60){
        $('.filterZoneScheda.open').css('width', 4*$('.filterInputContainer').width()+'px');
        var iconHeight = $('#filtersContainer').height()+$('.delModLists').height()+$('.filterInputContainer').height()*2*3;
        $('.filterZoneScheda.open').css('height', iconHeight+'px');
        $('.filterZoneScheda').css('right', 'unset');
        $('.filterZoneScheda').css('left', '5%');
    }

}


/***************************************************************************/

var settaDimensioniIconaFilterZoneClose = function(){

    var iconSize = $(window).height()*7/100;

    $('.filterZoneScheda.close').css('width', iconSize+'px');
    $('.filterZoneScheda.close').css('height', iconSize+'px');

    $('#openCloseFilterSearch').css('width', 'unset');
    $('#openCloseFilterSearch').css('float', 'unset');
    $('#openCloseFilterSearch').css('margin-right', 'unset');
    $('#openCloseFilterSearch').css('margin-top', 'unset');

    $('#openCloseFilterSearch a').css('font-size', (iconSize/2)+'px');

    if(filterZoneOpenWidthPerc == 70){
        $('.filterZoneScheda').css('right', '2.6%');
        $('.filterZoneScheda').css('left', 'unset');
    }

}


/********************************************************************************/
    $('.primaCol').unbind('click');


    $('input').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    $('textarea').unbind('mouseover').mouseover(function(){
        $(this).focus();
    });

    setTimeout(regolaDimensioniForEachHeader,2000)



    window.addEventListener('resize', function(){

        regolaDimensioniForEachHeader();
    });

    /* Imposto come "chiusa" la sezione di filtraggio e ricerca */

    var chiudiFilterSearch = function(){


        $('.filterZoneScheda').children().hide();
        $('#openCloseFilterSearch').show();
        $('#openCloseFilterSearch a').removeClass($('#openCloseFilterSearch a').attr('class'));
        $('#openCloseFilterSearch a').addClass('fa');
        $('#openCloseFilterSearch a').addClass('fa-wrench');
        $('.filterZoneScheda').addClass('close');
        $('.filterZoneScheda').removeClass('open');

        settaDimensioniIconaFilterZoneClose();
        $('#openCloseFilterSearch a').unbind('click');

        setTimeout(function(){
            $('.filterZoneScheda').unbind('click').click(function(){
                apriFilterSearch();
            });

        }, 50);

        tabellaSize = $(window).height()*65/100;
        regolaDimensioniForEachHeader();



    }

    var apriFilterSearch = function(){

        $('.filterZoneScheda').children().show();
        $('#openCloseFilterSearch a').removeClass($('#openCloseFilterSearch a').attr('class'));
        $('#openCloseFilterSearch a').addClass('fa');
        $('#openCloseFilterSearch a').addClass('fa-angle-double-up');
        $('.filterZoneScheda').removeClass('close');
        $('.filterZoneScheda').addClass('open');
        settaDimensioniIconaFilterZoneOpen();

        $('.filterZoneScheda').unbind('click');
        $('#openCloseFilterSearch a.fa-angle-double-up').click(function(){

            chiudiFilterSearch();
        });


        if( filterZoneOpenWidthPerc > 60 )
            tabellaSize = $(window).height()*40/100;
        else
            tabellaSize = $(window).height()*50/100;

        regolaDimensioniForEachHeader();

        //$('#openCloseFilterSearch a.fa-angle-double-up').parent().parent().unbind('click');

    }

    chiudiFilterSearch();

/*********************************************************/

    var startPosHeaderNewRow = $('#headerNewRow').height();

    if( startPosHeaderNewRow == 0 ){
        startPosHeaderNewRow = $('#tabellaContainerNewRow1').height();
    }

    $('#headerNewRow').css({'margin-top': '-'+startPosHeaderNewRow+'px'});

    $('#addRow').click(function(){
        $(this).unbind('click');
        $('#headerNewRow').animate({'margin-top': '+='+startPosHeaderNewRow+'px'});
        $('#tabellaContainerNewRow1 .datiScheda').children('td.primaCol').next().children('input').focus();

    });

    $('#delNewRow').click(function(){
        $('#headerNewRow').animate({'margin-top': '-='+startPosHeaderNewRow+'px'});

        $('#addRow').click(function(){
            $(this).unbind('click');
            $('#headerNewRow').animate({'margin-top': '+='+startPosHeaderNewRow+'px'});

        });

        pulisciHeaderNewRow();

    });
/*****************************************************************************/

    $('.datiScheda td').mouseenter(function(){

        $(this).children("input[type='number']").focus();
        $(this).children("input[type='text']").focus();
        $(this).children("textarea").focus();
        $(this).children('div').children("input[type='number']").focus();
        $(this).children('div').children("textarea").focus();
    });


/*****************************************************************************/

});