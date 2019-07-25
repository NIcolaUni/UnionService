class Home_dipendente extends OggettoBase {
    constructor(){
        super($('<div class="container-fluid" id="page-container"></div>'), null, $('body') );

        this.header = new Header(this, this.referenzaDOM);

        $('<div id="row-pagina" class="row"></div>').appendTo(this.referenzaDOM);

        this.attivita_base = new AttivitaBase(this, this.referenzaDOM.children('#row-pagina'));

        $('<div id="sezione_presentazione" class="col-md-8 col-sm-10"></div>').appendTo($('#row-pagina'));


        var id_in_slider = 0;
        this.note_page = new NotePage(this, $('#sezione_presentazione'), true, id_in_slider++); // 0
        this.agenda_page = new AgendaPage(this, $('#sezione_presentazione'), false, id_in_slider++); // 1
        this.calendario_page = new CalendarioPage(this, $('#sezione_presentazione'), false, id_in_slider++); // 2
        this.gestione_dip_page = new Gestione_dipPage(this, $('#sezione_presentazione'), false, id_in_slider++); // 3
        this.accogli_cliente_page = new Accogli_clientePage(this, $('#sezione_presentazione'), false, id_in_slider++); // 4
        this.email_page = new EmailPage(this, $('#sezione_presentazione'), false, id_in_slider++); // 5

        this.attivita_corrente = this.note_page;

        this.attivita_base.popolaActivityList();



    }

}