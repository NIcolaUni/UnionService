
//var oldAggiungiNotaBtnHtml;

var apriAggiungiNota = function(){

    $('div#addNotaBtn').children('a').hide();
    $('div#addNotaBtn').children('div#componi_nota').show();
    $('div#addNotaBtn').css({
        "width": "calc(100% - 47px)",
        "height": "calc(100% - 25px)",
        "border-radius": "2px",
        "top": "0",
        "z-index": "1",
        "box-shadow": "0 5px 8px rgba(0, 0, 0, 0.2)",
        "max-height": "300px",
        "overflow": "visible",
        "position": "relative",
        "margin": "0 auto",
        "right": "0",
        "cursor": "auto"
    });

    $('div#area_note_registrate').css('margin-top', '-43%');

    $('div#addNotaBtn').attr( 'onclick', '');
}

var sottolineaNotaVisionata = function($this) {
    var $labelMessaggioNota = $this.parent().parent().parent().children('.messaggio_nota_container').children('label');

    if($this.is(':checked'))
        $labelMessaggioNota.css('text-decoration', 'line-through' );
    else
        $labelMessaggioNota.css('text-decoration', 'none' );


}

$(function(){
    $('#annulla_nota').click(function(event){

        $('div#addNotaBtn').children('a').show();
        $('div#addNotaBtn').children('div#componi_nota').hide();
        $('div#addNotaBtn').attr('style', '');
        $('div#area_note_registrate').css('margin-top', '7%');

        $('div#addNotaBtn').attr( 'onclick', 'apriAggiungiNota()');
        event.stopImmediatePropagation()

    });
    $('')
});