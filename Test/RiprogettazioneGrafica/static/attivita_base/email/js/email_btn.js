class Email_btn extends Attivita_base_btn {

    constructor(oggettoGeneratore, $where_to_append, paginaAssociata){
        super($('<div class="attivitaBaseDipendente"> \
                    <a class="contactbutton" href="#"> \
                        <i class="fa fa-envelope"></i>Invia un email \
                    </a> \
                 <div>'), oggettoGeneratore, $where_to_append, "#40005F", paginaAssociata);


    }
}