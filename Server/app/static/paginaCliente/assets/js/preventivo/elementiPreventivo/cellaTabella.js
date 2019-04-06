class CellaTabella extends ElementoTabella{

    constructor(numeroColonna, cellaNascosta, oggettoGeneratore){
        super($('<td class="tdPreventivo"></td>'), oggettoGeneratore);

        this.numeroColonna = numeroColonna;
        this.cellaNascosta = cellaNascosta; //True se è una cella nascondibile, False altrimenti

    }

    settaContenuto(dato, tipoDato){

        if( tipoDato =='firstCol'){
            if( this.padre.rigaPrimaria ){
                this.referenzaDOM.html('<label>'+this.padre.id+'</label>'+dato );
            }

        }
        else {

            this.referenzaDOM.html(dato);
        }


    }

    settaDimensioni(dimensioni){
        this.referenzaDOM.css('width', dimensioni);
    }

    nascondiCella(attiva){
        /*attiva è un bool: True per celare la cella, False per mostrarla*/

        if( cellaNascosta ){ /* valuto prima di tutto se ho a che fare con una cella "nascondibile" */

            if( attiva ){
                this.referenzaDOM.hide();
            }
            else{
                this.referenzaDOM.show();
            }

        }
    }

}