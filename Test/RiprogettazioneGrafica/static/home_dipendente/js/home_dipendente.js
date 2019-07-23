class Home_dipendente extends OggettoBase {
    constructor(){
        super($('<div class="container-fluid" id="page-container"></div>'), null, $('body') );

        this.header = new Header(this, this.referenzaDOM);

        $('<div id="row-pagina" class="row"></div>').appendTo(this.referenzaDOM);

        this.attivita_base = new AttivitaBase(this, this.referenzaDOM.children('#row-pagina'));
        this.note_page = new NotePage(this, this.referenzaDOM.children('#row-pagina'));

    }

}