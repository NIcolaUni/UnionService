class EmailPage extends ActivityPage {

    constructor(oggettoGeneratore, $where_to_append, attivo, id_in_slider){
        super($('<div id="email_activity_container" class="activity_container"></div>'),
                    oggettoGeneratore, $where_to_append, attivo, id_in_slider);
    }
}