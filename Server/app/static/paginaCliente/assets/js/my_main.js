var difficoltaNascosta=true;

/*******************************************************************************************/
var modificaLivelloCliente = function( nome, cognome, indirizzo, valore){

       var newVal = parseInt(valore);
        var valoreAccettato = false;

        if( newVal == 1 ){
            valoreAccettato=true;
            newVal = 'facile'
        }
        else if( newVal == 2 ){
            valoreAccettato=true;
            newVal = 'media'
        }
        else if( newVal == 3 ){
            valoreAccettato=true;
            newVal = 'alta'
        }

        if( valoreAccettato ){
            socketCliente.emit('cambia_livello_difficolta', {
                'nome': nome,
                'cognome': cognome,
                'indirizzo': indirizzo,
                'valore': newVal
            })
        }
}

/************************************************************************************/

var settaAgenda = function(){

    var heightCal = $('div#agendaContainer').height()-300;

    $('#calendar').fullCalendar({
          header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
          },
          navLinks: true, // can click day/week names to navigate views
          //selectable: true,
         // selectHelper: true,
          editable: true,
          eventLimit: true, // allow "more" link when too many events
          //contentHeight: heightCal,
    });
}
/************************************************************************************/
var apriPaginaContabilita = function(){

    var chiaviPrev=$('#contabilitaSelect option:selected').attr('class').split(' ');

    var num_prev = chiaviPrev[0].split('-')[1];
    var revisione = chiaviPrev[1].split('-')[1];

    window.location = "/contabilitaCantiere/"+num_prev+"/"+revisione

}
/************************************************************************************/

$(function(){


    var offsetLabelDifficolta = $('div.inner').offset();
    var titleClientHeight = $('#nomeCliente').height();
    var difficoltaLabelHeight = $('label.difficoltaLabel').height();
    //  alert(offsetLabelDifficolta.top)
    $('.changeLivelloCliente').css('top', offsetLabelDifficolta.top+titleClientHeight-(difficoltaLabelHeight/8));

    settaAgenda();

    /*setto i bottoni di apertura/chiusura agenda*/
    $('#setSopraluogo').click(function(){
        $('#pageOverlay').show();
    });

    $('#closeAgendaBtn > a').click(function(){
        $('#pageOverlay').hide();
    });

    $('#closeAgendaBtn').click(function(){
        $('#closeAgendaBtn > a').trigger('click');
    });

    $('#showDifficolta').click(function(){

        if( difficoltaNascosta ){
            $('.difficoltaTitle').show();
            $('.difficoltaLabel').show();
            $('.changeLivelloCliente').css('display', 'inline-block');
            difficoltaNascosta=false;
        }
        else{
            $('.difficoltaTitle').hide();
            $('.difficoltaLabel').hide();
            $('.changeLivelloCliente').hide();
            difficoltaNascosta=true;
        }
    });

    var editClienteNascosti=true;

    $('#editCliente').click(function(){

        if( editClienteNascosti ){
            $('.editDato').show();
            editClienteNascosti=false;
        }
        else{
            $('.editDato').hide();
            editClienteNascosti=true;
        }

    });

    $('.editDato').click(function(){

        var tipoCampo =$(this).parent().children('h3').text()

        var toMod = ''
/*
        if( tipoCampo == 'Indirizzo:')
        if( tipoCampo == 'Telefono:')

        else if( tipoCampo == 'Email:')

        else if( tipoCampo == 'Lavorazione in corso:')*/


    });

});


/***********************************************************************************/