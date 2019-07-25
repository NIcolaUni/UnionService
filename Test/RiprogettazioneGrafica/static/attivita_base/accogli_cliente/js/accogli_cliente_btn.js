class Accogli_cliente_btn extends Attivita_base_btn {

    constructor(oggettoGeneratore, $where_to_append, paginaAssociata){
        super($('<div class="attivitaBaseDipendente"> \
                    <a class="accoglienzaButton" href="#"> \
                        <i class="fa fa-address-book-o"></i>Accogli <br> Cliente \
                    </a> \
                 <div>'), oggettoGeneratore, $where_to_append, "#674abf", paginaAssociata);

    }
}