class OggettoBase{
    constructor(referenzaDOM, oggettoGeneratore, $where_to_append ){
        this.referenzaDOM = referenzaDOM;
        this.padre = oggettoGeneratore;


        if( $where_to_append != null)
            this.referenzaDOM.appendTo($where_to_append);
    }

    settaReferenzaDOM(nuovaReferenzaJQuery){
        this.referenzaDOM = nuovaReferenzaJQuery;
    }


}