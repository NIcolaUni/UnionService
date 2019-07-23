class Search_bar extends OggettoBase{
    constructor(oggettoGeneratore, $where_to_append){
        super($('<div class="nav-item" id="search_client_form"> \
                    <form class="form-inline">  \
                    </form> \
                  </div>'), oggettoGeneratore, $where_to_append);

        this.input_search = $('<input class="form-control mr-sm-2" type="search" placeholder="Nome cliente" aria-label="Search">');
        this.btn_search = $('<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Cerca</button>');

        this.input_search.appendTo(this.referenzaDOM.children('form'));
        this.btn_search.appendTo(this.referenzaDOM.children('form'));
    }
}