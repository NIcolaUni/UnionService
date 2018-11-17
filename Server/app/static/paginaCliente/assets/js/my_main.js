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

/******************************************************************************/

$(function(){


          var offsetLabelDifficolta = $('div.inner').offset();
          var titleClientHeight = $('#nomeCliente').height();
          var difficoltaLabelHeight = $('label.difficoltaLabel').height();
        //  alert(offsetLabelDifficolta.top)
          $('.changeLivelloCliente').css('top', offsetLabelDifficolta.top+titleClientHeight-(difficoltaLabelHeight/8));


});


/***********************************************************************************/