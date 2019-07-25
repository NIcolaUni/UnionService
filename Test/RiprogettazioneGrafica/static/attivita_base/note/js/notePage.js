class NotePage extends ActivityPage {
    constructor(oggettoGeneratore, $where_to_append, attivo, id_in_slider){
        super($('<div id="note_activity_container" class="activity_container"> \
                        <div id="title_space" class="row"> \
                            <h2>Welcome  <span> Nicola Pancheri</span></h2> \
                              <p> <span class="orange">Commerciale dirigente </span></p> \
                        </div> \
                        <div id="note_space" class="row"> \
                        </div> \
                 </div>'), oggettoGeneratore, $where_to_append, attivo, id_in_slider);

        this.note = new NoteDipendente(this, this.referenzaDOM.children('#note_space'));

    }
}