class AreaNotifiche extends OggettoBase {
    constructor(oggettoGeneratore, $where_to_append){
        super($('<div id="areaNotifiche"> \
                    <div id="zonaTitolo_areaAlertChatHeader" class="row"><label></label></div> \
                    <div id="zonaContenuto_areaAlertChatHeader" class="row"></div> \
                 </div>'), oggettoGeneratore, $where_to_append);

        this.height ='200px';
        $('#zonaTitolo_areaAlertChatHeader').hide();
        $('#zonaContenuto_areaAlertChatHeader').hide();
    }

    apriChiudiAreaNotifiche( titolo ){

        if( $('#areaNotifiche').hasClass('opened') ){
            if(titolo != $('#zonaTitolo_areaAlertChatHeader').children('label').text()){
                $('#zonaTitolo_areaAlertChatHeader').children('label').remove();
                $('#zonaTitolo_areaAlertChatHeader').append($('<label>'+titolo+'</label>'));
            }
            else{
                $('#areaNotifiche').animate({'height' : '-='+this.height});
                $('#zonaTitolo_areaAlertChatHeader').hide();
                $('#zonaContenuto_areaAlertChatHeader').hide();
                $('#areaNotifiche').removeClass('opened');
            }
        }
        else{
            $('#areaNotifiche').animate({'height' : '+='+this.height});
            $('#areaNotifiche').addClass('opened');
            $('#zonaTitolo_areaAlertChatHeader').children('label').remove();
            $('#zonaTitolo_areaAlertChatHeader').append($('<label>'+titolo+'</label>'));
            $('#zonaTitolo_areaAlertChatHeader').show();
            $('#zonaContenuto_areaAlertChatHeader').show();
        }
    }


}