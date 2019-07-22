
class SelectTipologiaElemento extends ElementoPannelloControllo{

    constructor(id, titoloSelect, listaValori, oggettoGeneratore){
        super($('<div class="col-md-4">'+
                    '<span class="selectTipologiaElementoTitle">'+titoloSelect+'</span>'+
                    '<div class="selectContainer">'+
                        '<select class="js-select2" name="service">'+
                        '</select>'+
                        '<div class="dropDownSelect2"></div>'+
                    '</div>'+
                   '</div>'), oggettoGeneratore);
        this.id = id;
        this.listaValori = listaValori; // l'insieme dai valori che compongono il select

        this.tipologiaSelezionata = 0;


        popolaSelect();

        this.referenzaDOM.children('div.selectContainer').children('select').change(function(){

            this.comunicaIdSelect(parseInt($(this).children('option:selected').attr('class').split('-')[1]));
        });
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

    comunicaIdSelect(idOpzione){

        this.padre.modificaListaSelectElemento(this.id, idOpzione);

    }
}