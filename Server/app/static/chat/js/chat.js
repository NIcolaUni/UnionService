/***************************************************************************************/

var bloccaBlink = function(mittente, dipUsername){

    $('li.collega label.'+mittente).each(function(){

        $(this).removeClass('blink');

        socketChat.emit('messaggio_letto', {
            'mittente' : mittente,
            'destinatario' : dipUsername
        });
    });

    var countBlink = 0;

    $('li.collega label.blink').each(function(){

        countBlink++;
    });

    if( countBlink == 0 ){

        $('#openCloseChat a').removeClass('blink');
    }

}
/***************************************************************************************/

var attivaBlinkMessaggioNonLetto = function( mittente){

    $('#ulListColleghi label.'+mittente).addClass('blink');
    $('#openCloseChat a').addClass('blink');

    $('.blink').click(function(){
        $(this).removeClass('blink');

    });

}

/**************************************************************************************/
var inserisciBallonNuovoMessaggio =function(mittente, messaggio, dipUsername){

    $('.speech-wrapper').append(messaggio);

    var countBubble = 1;

    $('.bubble').each(function(){
        countBubble = countBubble+1;
    });

    var countBubble = countBubble;


    $('.speech-wrapper').animate({scrollTop: $('.speech-wrapper').height()*countBubble}, 0);

    socketChat.emit('messaggio_letto', {
            'mittente' : mittente,
            'destinatario' : dipUsername
    });

}
/************************************************************************************/
var creaChatBox = function(nomeCollega, collegaUsername){

    $(' <div id="chat-box" class="'+collegaUsername+'"> \
        <div id="chat-box-header"><label>'+nomeCollega+'</label><span id="controlChatBox"><a class="closeChatBox fa fa-close"></a></span></div> \
        <div class="speech-wrapper"> \
            <div class="bubble"> \
                <div class="txt"> \
                    <p class="name">Benni</p> \
                    <p class="message">Hey, check out this Pure CSS speech bubble...</p> \
                    <span class="timestamp">10:20 pm</span> \
                </div> \
                <div class="bubble-arrow"></div>\
            </div> \
            <div class="bubble alt"> \
                <div class="txt"> \
                    <p class="name alt">Benni</p> \
                    <p class="message">Hey, check out this Pure CSS speech bubble...</p> \
                    <span class="timestamp">10:20 pm</span> \
                </div> \
                <div class="bubble-arrow alt"></div>\
            </div> \
        </div> \
        <div id="chat-box-textField"><textarea id="msgToSend" placeholder="scrivi qualcosa..."></textarea></div> \
        <div id="button-chatBox"><button id="sendMessage">Invia</button></div> \
    </div>' ).insertAfter('.chat-div');


}

/**********************************************************************************/
var inviaMessaggio = function(mittente, destinatario){
    var msg=$('#msgToSend').val();

    if( msg != "" )
    {
        $('.speech-wrapper').append(
            '<div class="bubble alt"> \
                <div class="txt"> \
                    <p class="name alt">Io</p> \
                    <p class="message">'+msg+'</p><br/> \
                    <span class="timestamp timestampToSet"></span> \
                </div> \
                <div class="bubble-arrow alt"></div>\
            </div>'
        );

        var countBubble = 1;

        $('.bubble').each(function(){
            countBubble = countBubble+1;
        });

        var countBubble = countBubble;


        $('.speech-wrapper').animate({scrollTop: $('.speech-wrapper').height()*countBubble}, 0);

        socketChat.emit( "chat_message",
         {
            "mittente": mittente,
            "destinatario": destinatario,
            "testo": msg

         } );
        $('#msgToSend').val('');
    }
}

/***********************************************************************************/
var  apriChatBox = function($mittenteLabel, dipUsername){

    var collegaUsername = $mittenteLabel.attr('class').split(' ')[0];

    //$('.close-chat').trigger('click');
    $('.open-chat').trigger('click');
    $('#chat-box').remove();

    nomeCollega = $mittenteLabel.children('span').text();

    creaChatBox(nomeCollega, collegaUsername);

    socketChat.emit('storico_messaggi',
    {
        'mittente': dipUsername,
        'destinatario': collegaUsername,
    });

    $('.closeChatBox').click(function(){
        $(this).parent().parent().parent().remove();
    });

    $('#sendMessage').click(function(){

        inviaMessaggio(dipUsername, collegaUsername);

    });

}

/***********************************************************************************/
$(function(){
/*********************************************************************/
    /*
        Gestisco lo scorrimento a destra e sinistra della lista dei
        dipendente con cui chattare
    */

    var chat_opened=false;
    $('.chat-div').animate({"margin-right": '-=13%'});

    $(this).removeClass('open-chat');
    $(this).removeClass('fa-arrow-right');
    $(this).addClass('close-chat');
    $(this).addClass('fa-arrow-left')

    $('.close-chat').click(function(){

        if( chat_opened ){
            chat_opened=false;
            $('.chat-div').animate({"margin-right": '-=13%'});

            $(this).removeClass('open-chat');
            $(this).removeClass('fa-arrow-right');
            $(this).addClass('close-chat');
            $(this).addClass('fa-arrow-left');
            $('#chat-title').css('margin-left', '6%');

        }
        else{
            chat_opened=true;
            $('.chat-div').animate({"margin-right": '+=13%'});
            $(this).removeClass('close-chat');
            $(this).removeClass('fa-arrow-left')
            $(this).addClass('open-chat');
            $(this).addClass('fa-arrow-right');
            $('#chat-title').css('margin-left', '22%');

            setTimeout( function(){
                $(document).click(function(){
                    if( $('.chat-div:hover').length == 0){
                        $('.open-chat').trigger('click');
                        $(this).unbind('click')
                    }
                });

            }, 1000);

        }



    });

/***********************************************************************************************/

    $('.closeChatBox').click(function(){
        $(this).parent().parent().parent().remove()
    });
/***************************************************************************************************/

});


