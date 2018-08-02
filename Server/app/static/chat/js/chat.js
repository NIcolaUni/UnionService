 (function($) {

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
            $(this).addClass('fa-arrow-left')

        }
        else{
            chat_opened=true;
            $('.chat-div').animate({"margin-right": '+=13%'});
            $(this).removeClass('close-chat');
            $(this).removeClass('fa-arrow-left')
            $(this).addClass('open-chat');
            $(this).addClass('fa-arrow-right');

        }



    });

    $('.closeChatBox').click(function(){
        $(this).parent().parent().parent().remove()
    });



  }(window.jQuery));