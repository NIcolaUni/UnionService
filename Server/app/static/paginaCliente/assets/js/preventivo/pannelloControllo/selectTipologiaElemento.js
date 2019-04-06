class SelectTipologiaElemento{

    constructor(id, titoloSelect, listaValori){
        this.id = id;
        this.listaValori = listaValori; // l'insieme dai valori che compongono il select

        this.tipologiaSelezionata = 0

        this.referenzaDOM = $('<div class="col-md-4">'+
                                '<span class="selectTipologiaElementoTitle">'+titoloSelect+'</span>'+
                                '<div class="selectContainer">'+
                                    '<select class="js-select2" name="service">'+
                                    '</select>'+
                                    '<div class="dropDownSelect2"></div>'+
                                '</div>'+
                               '</div>');



        popolaSelect();
    }

    popolaSelect(){
        var id_option = 0;

        $.each(this.listaValori, function(index, valore){
            this.referenzaDOM.children('div.selectContainer').children('select').append($('<option class="opzione-'+id_option+'">'+valore+'</option>'));
            id_option++;
        });
    }

    modificaTipologiaSelezionata(idTipologia){
        this.tipologiaSelezionata=idTipologia;

    }
}