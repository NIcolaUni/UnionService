class AgendaPage extends ActivityPage {
    constructor(oggettoGeneratore, $where_to_append, attivo, id_in_slider){
        super($('<div id="agenda_activity_container" class="activity_container"> \
                    <div id="agenda_space"> \
                        <div id="agenda"></div> \
                    </div> \
                 </div>'), oggettoGeneratore, $where_to_append, attivo, id_in_slider);



        var calendarEl = document.getElementById('agenda');

        this.agenda_fullcalendar = new FullCalendar.Calendar( calendarEl, {
            plugins: [ 'interaction', 'dayGrid' ],
            header: {
                left: 'prevYear,prev,next,nextYear today',
                center: 'title',
                right: 'dayGridMonth,dayGridWeek,dayGridDay'
            },
            defaultDate: '2019-06-12',
            navLinks: true, // can click day/week names to navigate views
            editable: true,
            height: 'parent',
            eventLimit: true, // allow "more" link when too many events
            events: [
                {
                    title: 'All Day Event',
                    start: '2019-06-01'
                },
                {
                    title: 'Long Event',
                    start: '2019-06-07',
                    end: '2019-06-10'
                },
                {
                    groupId: 999,
                    title: 'Repeating Event',
                    start: '2019-06-09T16:00:00'
                },
                {
                    groupId: 999,
                    title: 'Repeating Event',
                    start: '2019-06-16T16:00:00'
                },
                {
                    title: 'Conference',
                    start: '2019-06-11',
                    end: '2019-06-13'
                },
                {
                    title: 'Meeting',
                    start: '2019-06-12T10:30:00',
                    end: '2019-06-12T12:30:00'
                }

            ]
        });



    }
}