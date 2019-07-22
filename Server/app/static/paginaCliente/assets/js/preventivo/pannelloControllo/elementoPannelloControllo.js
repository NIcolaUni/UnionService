class ElementoPannelloControllo{

    constructor(referenzaDOM, oggettoGeneratore){
       this.referenzaDOM = referenzaDOM;
       this.padre = oggettoGeneratore;
    }

    settaReferenzaDOM(nuovaReferenzaJQuery){
        this.referenzaDOM = nuovaReferenzaJQuery;
    }
}