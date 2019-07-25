class ActivityPage extends OggettoBase {
    constructor(referenzaDOM, oggettoGeneratore, $where_to_append, attivo, id_in_slider){
        super(referenzaDOM, oggettoGeneratore, $where_to_append);

        this.id_in_slider = id_in_slider;

        if(!attivo)
            this.referenzaDOM.css('visibility', 'hidden');
    }
}