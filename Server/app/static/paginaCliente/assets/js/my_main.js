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

var modificaDatiCliente = function($this){

    var datoToMod;
    alert($this.attr('id'))
    if( $this.attr('id') == 'selectTipologiaCliente' ){
        datoToMod = 'tipologia';
    }
    else{
        datoToMod = $this.attr('class').split(' ')[0];
    }


    var datoToPrint = datoToMod + ' cliente';

    var formToAsk = [];

    var nomeSalvato = $('h1#nomeCliente').text().split(' ')[0];
    var cognomeSalvato = $('#nomeCliente').text().split(' ')[1];
    var telefonoSalvato;
    var emailSalvata;
    var indirizzoSalvato = $('a.editDato.indirizzo').parent().children('span').text();
    var via, civico, regione, cap;
    var lavorazioneSalvata;


    if( datoToMod == 'nomeCliente'){

        datoToPrint = 'nome e cognome del cliente';
        formToAsk.push({ id: 'nome',  type: 'text', label: 'Nome:', name: 'nome', value: nomeSalvato});
        formToAsk.push({ id: 'cognome',  type: 'text', label: 'Cognome:', name: 'cognome', value: cognomeSalvato });
    }
    else if( datoToMod == 'telefono' ){

        telefonoSalvato = $this.parent().children('span').text();
        formToAsk.push({ id: 'telefono',  type: 'text', label: 'Telefono:', name: 'telefono', value: telefonoSalvato });

    }
    else if( datoToMod == 'email' ){
        emailSalvata = $this.parent().children('span').text();
        formToAsk.push({ id: 'email',  type: 'text', label: 'Email:', name: 'email', value: emailSalvata });

    }
    else if( datoToMod == 'indirizzo' ){


        var splittedAddr = indirizzoSalvato.split(', ');
        via= splittedAddr[0].split(' ')[0];
        civico= splittedAddr[0].split(' ')[1];
        regione = splittedAddr[1].split(' ')[0];
        cap = splittedAddr[1].split(' ')[1];

        formToAsk.push({ id: 'via',  type: 'text', label: 'Via:', name: 'via', value:  via });
        formToAsk.push({ id: 'civico',  type: 'text', label: 'Civico:', name: 'civico', value:  civico });
        formToAsk.push({ id: 'regione',  type: 'text', label: 'Regione:', name: 'regione', value:  regione });
        formToAsk.push({ id: 'cap',  type: 'text', label: 'CAP:', name: 'cap', value:  cap });

    }
    else if( datoToMod == 'lavorazione' ){
        datoToPrint = 'lavorazione in corso';
        lavorazioneSalvata = $this.parent().children('span').text();
        formToAsk.push({ id: 'lavorazione',  type: 'text', label: 'Lavorazione in corso:', name: 'lavorazione', value: lavorazioneSalvata });

    }
    else if( datoToMod == 'tipologia' ){
        alert('slnoo')
        socketCliente.emit('modificaDatiCliente', {
                'oldNome': nomeSalvato,
                'oldCognome': cognomeSalvato,
                'oldIndirizzo': indirizzoSalvato,
                'toMod' : datoToMod,
                'val1' : $('#selectTipologiaCliente').val()

            });
        return;
    }



    swal.withFormAsync({
        title: 'Modifica ' + datoToPrint,
        showCancelButton: true,
        confirmButtonColor: '#DD6B55',
        confirmButtonText: 'Ok',
        cancelButtonText: 'annulla',
        closeOnConfirm: true,
        formFields: formToAsk,
    }).then(function (context) {
        if(context._isConfirm){
            var val1 = '';
            var val2 = '';
            var val3 = '';
            var val4 = '';


            if( datoToMod == 'nomeCliente' ){
                val1 = context.swalForm['nome'];
                val2 = context.swalForm['cognome'];

                $('h1#nomeCliente').text(val1 + ' ' + val2);

            }else if( datoToMod == 'indirizzo'){
                val1 = context.swalForm['via'];
                val2 = context.swalForm['civico'];
                val3 = context.swalForm['regione'];
                val4 = context.swalForm['cap'];

                $this.parent().children('span').text( val1 + ' '+ val2+ ', '+ val3 + ' '+val4 );


            }else if( datoToMod == 'telefono'){
                val1 = context.swalForm['telefono'];
                if( val1.length > 12){
                    alert('errore: numero troppo lungo');
                    return;
                }
                $this.parent().children('span').text(val1);

            }else if( datoToMod == 'email' ){
                val1 = context.swalForm['email'];
                $this.parent().children('span').text(val1);

            }else if( datoToMod == 'lavorazione'){
                val1 = context.swalForm['lavorazione'];
                if( val1.length > 500 ){
                    alert('errore:  descrizione della lavorazione troppo lunga');
                    return;
                }
                $this.parent().children('span').text(val1);
            }

            socketCliente.emit('modificaDatiCliente', {
                'oldNome': nomeSalvato,
                'oldCognome': cognomeSalvato,
                'oldIndirizzo': indirizzoSalvato,
                'toMod' : datoToMod,
                'val1' : val1,
                'val2'  : val2,
                'val3': val3,
                'val4': val4
            });
        }

    });

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

            $('#tipologiaCliente').text('Tipologia:');
            $('#selectTipologiaCliente').show();
            $('#tipologiaClienteContainer').css( 'width', '26%' );
            editClienteNascosti=false;
        }
        else{
            $('.editDato').hide();

            $('#tipologiaCliente').text('Tipologia: '+$('#selectTipologiaCliente').val());
            $('#selectTipologiaCliente').hide();
             $('#tipologiaClienteContainer').css( 'width', 'unset' );
            editClienteNascosti=true;
        }

    });



});


/***********************************************************************************/