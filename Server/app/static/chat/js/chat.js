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

    $('.closeChatBox').click(function(){
        $(this).parent().parent().parent().remove()
    });



  }(window.jQuery));