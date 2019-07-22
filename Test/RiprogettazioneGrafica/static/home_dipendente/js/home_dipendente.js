var aggiungiFunzionalitaDipendenteBase = function (){

    for( var i = 0; i < 6; i++){
        if( i == 0 ){
            $('#base_activity_slider_wrapper').append('<div class="attivitaBaseDipendente" style="background:#08021b"><a class="homebutton active" href="#"><i class="fa fa-home"></i>Home</a><div>');

        }
        else if( i == 1 ){
            $('#base_activity_slider_wrapper').append('<div class="attivitaBaseDipendente" style="background:#110633"><a class="agendaButton" href="#"><i class="fa fa-book"></i>Agenda</a><div>');

        }
        else if( i == 2 ){
            $('#base_activity_slider_wrapper').append('<div class="attivitaBaseDipendente" style="background:#251163"><a class="calendarButton" href="#"><i class="fa fa-calendar"></i>Calendario</a><div>');

        }
        else if( i == 3 ){
            $('#base_activity_slider_wrapper').append('<div class="attivitaBaseDipendente" style="background:#3b19a5"><a class="gestioneDipButton" href="#"><i class="fa fa-user-plus"></i>Gestione <br> Dipendenti</a><div>');

        }
        else if( i == 4 ){
            $('#base_activity_slider_wrapper').append('<div class="attivitaBaseDipendente" style="background:#674abf"><a class="accoglienzaButton" href="#"><i class="fa fa-address-book-o"></i>Accogli <br> Cliente</a><div>');

        }
        else if( i == 5 ){
            $('#base_activity_slider_wrapper').append('<div class="attivitaBaseDipendente" style="background:#40005F"><a class="contactbutton" href="#"><i class="fa fa-envelope"></i>Invia un email</a><div>');

        }

    }
}

