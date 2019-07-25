class Gestione_dip_btn extends Attivita_base_btn {

    constructor(oggettoGeneratore, $where_to_append, paginaAssociata){
        super($('<div class="attivitaBaseDipendente"> \
                    <a class="gestioneDipButton" href="#"> \
                        <i class="fa fa-user-plus"></i>Gestione <br> Dipendenti \
                    </a> \
                 <div>'), oggettoGeneratore, $where_to_append, "#3b19a5", paginaAssociata);

    }
}