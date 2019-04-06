/******************************************************************************************/
/*
    Funzioni per implementare il riordinamento delle righe tramite Drug n Drop
*/

var bloccaDrugFunctionality = function(){
    $('tBody').removeClass('ui-sortable');
    $('tBody').removeClass('ui-sortable-handle');
}

var startStopOrdinamentoLavorazioni = function($this){

    if( righeLavInOrdinamento ){
        righeLavInOrdinamento = false;
        mostraFootLav();
        rienumeraPagina();

        $("tbody").sortable("destroy");
    }
    else{
        righeLavInOrdinamento = true;
        nascondiFootLav($this);

        $('tbody').sortable({

            stop: function(){
                rienumeraPagina();

            }
        });
    }
}

/*******************************************************************************************/

class RigaTabella extends ElementoTabella{

    constructor(id, primaria, grandezzeCelle, datiCelle, tipoDatoCelle, oggettoGeneratore){
         /*
            grandezzeCelle, datiCelle, tipoDatoCelle sono tutti array della stessa lunhgezza ovvero
            del numero di colonne della tabella
        */
        super(null, oggettoGeneratore);
        this.id=id;
        this.primaria = primaria;//booleano
        this.listaCelle = [];

    }


    popolaRiga(datiCelle, tipoDatoCelle, listaColonneVisibili){
        $.each(datiCelle, function(index, el){
            var nuovaCella = new CellaPreventivo(index, !listaColonneVisibili[index], primaria, this);
            nuovaCella.settaContenuto(el, tipoDatoCelle[index]);
            nuovaCella.settaDimensioni(grandezzeCelle[index]);

            this.listaCelle.push(nuovaCella);
        });



        this.listaCelle.forEach(function(el){
            this.referenzaDOM.append(el.referenzaDOM);
        });

    }

}

class RigaSecondaria extends RigaTabella {
    constructor(id, grandezzeCelle, datiCelle, tipoDatoCelle, oggettoGeneratore){
        super(id, false, grandezzeCelle, datiCelle, tipoDatoCelle, oggettoGeneratore);


        this.settaReferenzaDOM(
            $('<tr id="'oggettoGeneratore.id+'_rigaSecondaria-'+this.padre.id+'-'+id+' class="rigaPreventivo rigaSecondaria"></tr>')
        );

        this.popolaRiga(datiCelle, tipoDatoCelle, oggettoGeneratore.padre.padre.listaColonneVisibili);

    }
}

class RigaPrimaria extends RigaTabella {

    constructor(id, datiCelle, tipoDatoCelle, oggettoGeneratore){
        super(id, true, oggettoGeneratore.padre.grandezzeCelle, datiCelle, tipoDatoCelle, oggettoGeneratore);

        this.listaRigheSecondarie = [];

        this.settaReferenzaDOM(
            $('<tr id="'oggettoGeneratore.id+'_rigaPrimaria-'+id+' class="rigaPreventivo rigaPrimaria" onclick="bloccaDrugFunctionality();" ondblclick="startStopOrdinamentoLavorazioni($(this));" ></tr>')
        );

        this.popolaRiga(datiCelle, tipoDatoCelle, oggettoGeneratore.padre.listaColonneVisibili);


    }

    aggiungiRigaSecondaria(datiCelle, tipoDatoCelle){
        var nuovaRigaSecondaria = RigaSecondaria(this.listaRigheSecondarie.length, this.padre.padre.grandezzeCelle, datiCelle, tipoDatoCelle, this);

        this.listaRigheSecondarie.push(nuovaRigaSecondaria);
        this.referenzaDOM.append(nuovaRigaSecondaria);
    }

    togliRigaSecondaria(){

    }

    riordinaListaRigheSecondarie(){

    }
}

