
  var usPopupPrezzari = function(parametriPopup){

    var box=parametriPopup['clicckedButton'];
    var docWrapper=parametriPopup['popupContainer'];
    var bodyPopup=parametriPopup['popupBodyContent'];
    var titolo=parametriPopup['popupTitle'];
    var funzionePostPopup=parametriPopup['popupFunction'];
    var content_popup_classes=parametriPopup['content_popup_classes'];
    var body_popup_classes = parametriPopup['body_popup_classes'];


    if( content_popup_classes === undefined ){
        content_popup_classes=''
    }

    if( body_popup_classes === undefined ){

        body_popup_classes='';
    }

    box.each(function(){

        $(this).unbind('click').click(function(){

            $clicckedBtn=$(this)

            if( $(this).hasClass('popped') ){
                $(this).removeClass('popped');
                $('.popup-overlay').remove();
            }
            else{

                /*previene problemi sulla chiusura/apertura dei popup*/
                $('.popped').each(function(){
                    $(this).removeClass('popped');
                });

                $('.popup-overlay').remove();
                $(this).addClass('popped')
                var popup=$('<div class="popup-overlay"><div class="popup-content active '+content_popup_classes+'">'+
                             '<div class="titleContainer"><label class="titlePopup">'+
                              titolo+'</label><a class="fa fa-close close-popup"></a></div>'+
                              '<div class="body-popup '+body_popup_classes+'">'+
                              bodyPopup+'</div></div></div>').appendTo('#'+docWrapper.attr('id'));

                var offset = $(this).offset();
                var top = offset.top + $(this).outerHeight() + 15;

                var left = offset.left-($(this).outerWidth()/2);

                if(left < -3){
                  popup.children('.popup-content').addClass('rightSide');
                  popup.css({
                              'left': offset.left+$(this).outerWidth(),
                              'top': offset.top -($(this).outerHeight()/2)
                  });
                }
                else{
                  popup.children('.popup-content').addClass('bottomSide');
                  popup.css({
                              'left': offset.left-($(this).outerWidth()/2)-1,
                              'top': offset.top -$(this).outerHeight()*2+10
                  });
                }

                funzionePostPopup($(this));

                $('.close-popup').click(function(){
                    $('.popup-overlay').remove();
                });


                /* se clicco ovunque nel documento ( tranne sul popup) elimino il popup*/
                setTimeout( function(){
                    $(document).click(function(){
                        if( $('.popup-overlay:hover').length == 0){
                            popup.remove();
                            $clicckedBtn.removeClass('popped');
                            $(this).unbind('click')
                        }
                    });

                }, 1000);



            }


        });


    });



  }


  var usPopupProdotti = function(parametriPopup){

    var box=parametriPopup['clicckedButton'];
    var docWrapper=parametriPopup['popupContainer'];
    var bodyPopup=parametriPopup['popupBodyContent'];
    var titolo=parametriPopup['popupTitle'];
    var funzionePostPopup=parametriPopup['popupFunction'];
    var content_popup_classes=parametriPopup['content_popup_classes'];
    var body_popup_classes = parametriPopup['body_popup_classes'];

    var inTable = parametriPopup['inTable'];


    if( content_popup_classes === undefined ){
        content_popup_classes=''
    }

    if( body_popup_classes === undefined ){

        body_popup_classes='';
    }

    box.each(function(){



        $clicckedBtn=$(this)

        if( $(this).hasClass('popped') ){
            $(this).removeClass('popped');
            $('.popup-overlay').remove();
        }
        else{

            /*previene problemi sulla chiusura/apertura dei popup*/
            $('.popped').each(function(){
                $(this).removeClass('popped');
            });

            $('.popup-overlay').remove();
            $(this).addClass('popped')
            var popup=$('<div class="popup-overlay mini"><div class="popup-content active '+content_popup_classes+'">'+
                         '<div class="titleContainer"><label class="titlePopup">'+
                          titolo+'</label><a class="fa fa-close close-popup"></a></div>'+
                          '<div class="body-popup '+body_popup_classes+'">'+
                          bodyPopup+'</div></div></div>').appendTo('#'+docWrapper.attr('id'));

            $('.popup-overlay.mini').css('width', '13%');

            if( inTable ){
                popup.children('.popup-content').addClass('topSideProdotti');
                var offset = $clicckedBtn.offset();
                var left = offset.left-20;


                var top = ($clicckedBtn.offset().top- docWrapper.offset().top)- popup.innerHeight()//+20//-( popup.height()*10/100);

                popup.css({
                  'left': left,
                  'top':  top
                });


            }
            else{
                popup.children('.popup-content').addClass('bottomSideProdotti');
                var offset = $clicckedBtn.offset();
                var left = offset.left-docWrapper.offset().left-$clicckedBtn.width();
                var top= $clicckedBtn.offset().top+2*$clicckedBtn.innerHeight();

                popup.css({
                  'left': left,
                  'top':  top
                });

            }


            funzionePostPopup($(this));

            $('.close-popup').click(function(){
                $('.popup-overlay').remove();
            });


            /* se clicco ovunque nel documento ( tranne sul popup) elimino il popup*/
            setTimeout( function(){
                $(document).click(function(){
                    if( $('.popup-overlay:hover').length == 0){
                        popup.remove();
                        $clicckedBtn.removeClass('popped');
                       // $(this).unbind('click')
                    }
                });

            }, 1000);



        }



    });



  }
