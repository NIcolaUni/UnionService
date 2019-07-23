class RaggruppamentoIcone extends OggettoBase {

    constructor(oggettoGeneratore, $where_to_append){
        super($('<div id="raggruppamento-header-right" class="raggruppamento-nav-item"> \
                    <div class="nav-item" id="chat_icon"> \
                    </div> \
                    <div class="nav-item" id="alert_icon"> \
                    </div> \
                    <div class="nav-item" id="control_panel_icon"> \
                    </div> \
                 </div>'), oggettoGeneratore, $where_to_append);

        this.areaNotifiche = new AreaNotifiche(this, this.referenzaDOM);

        this.chat = $('<a class="nav-link headerItem fa fa-comments-o"></a>');
        this.alert = $('<a class="nav-link headerItem fa fa-bell"></a>');
        this.control_panel = new Control_panel(this, $('#page-container'), this.referenzaDOM.children('#control_panel_icon'));

        this.chat.appendTo(this.referenzaDOM.children('#chat_icon'));
        this.alert.appendTo(this.referenzaDOM.children('#alert_icon'));

        var thisRef = this;
        this.chat.click(function(){
            thisRef.areaNotifiche.apriChiudiAreaNotifiche('CHAT');
        });

        this.alert.click(function(){
            thisRef.areaNotifiche.apriChiudiAreaNotifiche('NOTIFICHE');
        });
    }


}