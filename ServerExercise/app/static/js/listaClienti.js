(function($) {

  var $listaClienti = $('#listaClienti');
  var $body = $('body');

  $listaClienti._locked = false;

  $listaClienti._lock = function() {

    if ($listaClienti._locked)
      return false;

    $listaClienti._locked = true;

    window.setTimeout(function() {
      $listaClienti._locked = false;
    }, 350);

    return true;

  };

  $listaClienti._show = function() {

    if ($listaClienti._lock())
      $body.addClass('is-listaClienti-visible');

  };

  $listaClienti._hide = function() {

    if ($listaClienti._lock())
      $body.removeClass('is-listaClienti-visible');

  };

  $listaClienti._toggle = function() {

    if ($listaClienti._lock())
      $body.toggleClass('is-listaClienti-visible');

  };

  $listaClienti
    .appendTo($body)
      .click(function(event) {
					event.stopPropagation();
					// Hide.
					$listaClienti._hide();

			});

  $('#listaClienti div.inner').click(function(event) {
		  event.stopPropagation();
	});

  $('#listaClienti a.close').click(function(event) {

			event.preventDefault();
			event.stopPropagation();
			event.stopImmediatePropagation();
			// Hide.
			$listaClienti._hide();

	});

  $('#listaClienti a').click( function(event) {

			var href = $(this).attr('href');

			event.preventDefault();
			event.stopPropagation();

			// Hide.
				$listaClienti._hide();

			// Redirect.
				window.setTimeout(function() {
					window.location.href = href;
				}, 350);

	});


  $('input.cercaCliente').click(function(event){
    event.stopPropagation();
    event.preventDefault();

    // Toggle.
    $listaClienti._toggle();

	}).on('keydown', function(event) {

			// Hide on escape.
			if (event.keyCode == 27)
				$listaClienti._hide();

	});


})(jQuery);
