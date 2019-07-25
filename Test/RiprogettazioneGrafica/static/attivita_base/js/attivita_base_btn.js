class Attivita_base_btn  extends OggettoBase {

    constructor( referenzaDOM, oggettoGeneratore, $where_to_append, color, paginaAssociata){
        super(  referenzaDOM, oggettoGeneratore, $where_to_append);

        this.paginaAssociata = paginaAssociata;
        this.color = color;
        this.active_color = "#feca08";

        this.paginaDisattiva();
    }

    abilitaBottone(presentazionePaginaFunction, height_pagine){

        var thisRef = this;
        this.referenzaDOM.click(function(){
            presentazionePaginaFunction( height_pagine, thisRef)
        });
    }

    paginaAttiva(){
        this.referenzaDOM.css('background', this.active_color);
    }

    paginaDisattiva(){
        this.referenzaDOM.css('background', this.color);
    }
}