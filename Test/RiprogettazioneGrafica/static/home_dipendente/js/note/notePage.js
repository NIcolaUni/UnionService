class NotePage extends OggettoBase {
    constructor(oggettoGeneratore, $where_to_append){
        super($('<div class="col-md-8 col-sm-10"> \
                    <div id="title_space" class="row"> \
                        <h2>Welcome  <span> Nicola Pancheri</span></h2> \
                          <p> <span class="orange">Commerciale dirigente </span></p> \
                    </div> \
                    <div id="note_space" class="row"> \
                    </div> \
                 </div>'), oggettoGeneratore, $where_to_append);

        this.note = new NoteDipendente(this, this.referenzaDOM.children('#note_space'));
    }
}