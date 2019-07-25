class Calendario_btn extends Attivita_base_btn {

    constructor(oggettoGeneratore, $where_to_append, paginaAssociata){
        super($('<div class="attivitaBaseDipendente"> \
                    <a class="calendarButton" href="#"> \
                        <i class="fa fa-calendar"></i>Calendario \
                    </a> \
                 <div>'), oggettoGeneratore, $where_to_append, "#251163", paginaAssociata);

        this.calendario_rendered = false;

        var thisRef = this;
        this.referenzaDOM.click(function(){
            if(!thisRef.calendario_rendered){
                thisRef.paginaAssociata.renderCalendario();
                thisRef.calendario_rendered = true;
            }
        });

    }


}