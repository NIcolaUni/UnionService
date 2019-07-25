class Agenda_btn extends Attivita_base_btn {

    constructor(oggettoGeneratore, $where_to_append, paginaAssociata){
        super($('<div class="attivitaBaseDipendente"> \
                    <a class="agendaButton" href="#">  \
                        <i class="fa fa-book"></i>Agenda \
                    </a> \
                  <div>'), oggettoGeneratore, $where_to_append, "#110633", paginaAssociata);

        this.agenda_rendered = false;

        var thisRef = this;

        this.referenzaDOM.click(function(){
            if(!thisRef.agenda_rendered){
                thisRef.paginaAssociata.agenda_fullcalendar.render();
                thisRef.agenda_rendered = true;
            }

        });

    }


}