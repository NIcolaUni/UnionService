class SelectTipologiaElemento{

    constructor(id, titoloSelect, listaValori){
        this.id = id;
        this.listaValori = listaValori; // l'insieme dai valori che compongono il select

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
        $.each(this.listaValori, function(index, valore){
            this.referenzaDOM.children('div.selectContainer').children('select').append($('<option>'+valore+'</option>'));
        });
    }
}