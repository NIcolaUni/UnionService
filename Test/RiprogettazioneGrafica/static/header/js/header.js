class Header extends OggettoBase{

    constructor(oggettoGeneratore, $where_to_append){
        super($('<nav class="navbar navbar-expand-sm header_home"> \
                    <div  class="header-section" id="header_left"> \
                        <div class="nav-item"> \
                        </div> \
                    </div> \
                    <div class="header-section" id="header_right"> \
                    </div> \
                  </nav>'), oggettoGeneratore, $where_to_append);

        this.logo_azienda = $('<a id="logoAzienda"><img src="static/img/logo-azienda.png"></a>');
        this.logo_azienda.appendTo(this.referenzaDOM.children('#header_left').children('.nav-item'));

        this.search_bar = new Search_bar(this, this.referenzaDOM.children('#header_right'));
        this.raggruppamentoIcone = new RaggruppamentoIcone(this, this.referenzaDOM.children('#header_right'));

    }
}