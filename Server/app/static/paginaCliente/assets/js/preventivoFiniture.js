
/*****************************************************************************************************/

var suddividiProdotiiPerModello = function(listaProdottiPerMarchio, listaModelliDistinti){

    /*
        Input:
        - listaProdottiPerMarchio = [ [nome_tipologia, [[nome_marchio, [[nome_modello, nome_prodotto],...]],...] ], ... ]
        - listaModelliDistinti = [nome_modello]

        Output:

        - marchiPerTipologia = [ [ nome_tipologia, [[nome_marchio, [[nome_modello, [nome_prodotto]],...]],...] ], ... ]

    */

    var marchiPerTipologia = [];

    // per ogni tipologia
    listaProdottiPerMarchio.forEach(function(tipologia){

        var modelliPerMarchio = [];

        // per ogni marchio
        tipologia[1].forEach(function(marchio){

            var prodottiPerModello = [];

            listaModelliDistinti.forEach(function(modello){

                var listProdotti = [];

                //per ogni prodotto
                marchio[1].forEach(function(prodotto){

                    if( prodotto[0] == modello ){
                        listProdotti.push(prodotto[1])
                    }

                });

                prodottiPerModello.push([modello, listProdotti])

            });


            modelliPerMarchio.push([marchio, prodottiPerModello]);

        });

        marchiPerTipologia.push([tipologia, modelliPerMarchio]);

    });

    return marchiPerTipologia;


}
/****************************************************************************************************/

var suddividiProdottiPerMarchio = function(listaProdottiPerTipologia, listaMarchiDistinti){

    /*
        Input:
        - listaProdottiPerTipologia = [ [nome_tipologia, [[nome_marchio, nome_modello, nome_prodotto], ...]], ...]
        - listaMarchiDistiniti = [ nome_marchio ]

        Output:

        - marchiPerTipologia = [ [nome_tipologia, [[nome_marchio, [[nome_modello, nome_prodotto],...]],...] ], ... ]


    */

    var marchiPerTipologia = [];

    listaProdottiPerTipologia.forEach(function(tipologia){

        var prodottiPerMarchio = [];

        listaMarchiDistinti.forEach(function(marchio){

            var listProdotti = [];

            tipologia[1].forEach(function(prodotto){

                if(prodotto[0] == marchio){

                    listProdotti.push([ prodotto[1], prodotto[2] ]);
                }
            });

            prodottiPerMarchio.push([marchio, listProdotti])

        });

        marchiPerTipologia.push([tipologia, prodottiPerMarchio]);

    });

    return marchiPerTipologia;

}

/*************************************************************************/

var suddividiProdottiPerTipologiaMarchioModello = function(listaProdottiPerTipologia, listaMarchiDistinti, listaModelliDistinti){

    var prodottiPerTipologiaMarchio = suddividiProdottiPerMarchio( listaProdottiPerTipologia, listaMarchiDistinti );

    return suddividiProdotiiPerModello( prodottiPerTipologiaMarchio, listaModelliDistinti )

}

/*************************************************************************/

var aggiungiProdottiToSelectElement = function( listaProdottiPerTipologia, listaMarchiDistinti, listaModelliDistinti){

    var prodottiPerTipologiaMarchioModello = suddividiProdottiPerTipologiaMarchioModello( listaProdottiPerTipologia, listaMarchiDistinti, listaModelliDistinti );

    var counterTipologia = 0;
    prodottiPerTipologiaMarchioModello.forEach(function(tipologia){

        $('#selectTipologia').append('<option class="tipologia-'+counterTipologia+'">'+tipologia[0]+'</option>');

        var counterMarchio = 0;
        tipologia[1].forEach(function(marchio){

            $('#selectMarchio').append('<option class="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'">'+marchio[0]+'</option>');

            var counterModello = 0;
            marchio[1].forEach(function(modello){

                $('#selectModello').append('<option class="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'_modello-'+counterModello+'">'+modello[0]+'</option>');

                var counterProdotto = 0;
                modello[1].forEach(function(prodotto){

                    $('#listaElementPreventivo').append(
                         '<li><button id="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'_modello-'+counterModello+'_prodotto-'+counterProdotto+'" class="elementFattura">'+
                         '<label for="tipologia-'+counterTipologia+'_marchio-'+counterMarchio+'_modello-'+counterModello+'_prodotto-'+counterProdotto+'">'+prodotto+'</label></button></li>'
                    );

                    counterProdotto++;
                });

                counterModello++;
            });

            counterMarchio++;
        });

        counterTipologia++;

    });

}

/************************************************************************/