class Note_btn extends Attivita_base_btn {

    constructor(oggettoGeneratore, $where_to_append, paginaAssociata){
        super($('<div class="attivitaBaseDipendente" > \
                    <a class="homebutton active" href="#"> \
                        <i class="fa fa-home"></i>Home \
                    </a> \
                 <div>'), oggettoGeneratore, $where_to_append, "#08021b", paginaAssociata);

    }
}