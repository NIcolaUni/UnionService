(function($) {


	$('.side-button a.btn').click(function(){

			if( $('.immagine-bottone').hasClass('fa-chevron-left')){

				$('.immagine-bottone').removeClass('fa-chevron-left');
				$('.immagine-bottone').addClass('fa-chevron-right');
				$('#chat-section').animate({"right":"0px"}, "slow");
				$('.side-button').animate({"right":"310px"}, "slow");
			}
			else if( $('.immagine-bottone').hasClass('fa-chevron-right') ){

				$('.immagine-bottone').removeClass('fa-chevron-right');
				$('.immagine-bottone').addClass('fa-chevron-left');
				$('#chat-section').animate({"right":"-300px"}, "slow");
				$('.side-button').animate({"right":"5px"}, "slow");


			}

	});

	$('.toggle-menu').click(function(){
        $('.show-menu').stop(true,true).slideToggle();
        return false;
  });


	$('.show-menu a').click(function() {
    	$('.show-menu').fadeOut('slow');
  });


	$(".main-menu a").click(function(){
		var id =  $(this).attr('class');
		id = id.split('-');
		$('a.active').removeClass('active');
	  	$(this).addClass('active');
		$("#menu-container .content").slideUp('slow');
		$("#menu-container .homepage").slideUp('slow');
		$("#menu-container #menu-"+id[1]).slideDown('slow');

		return false;
	});

	$(".main-menu a.homebutton").click(function(){
			$("#menu-container .homepage").slideDown('slow');

			return false;
	});

	$(".main-menu a.registraDipButton").click(function(){
			$("#menu-container .registraDip-section").slideDown('slow');

			return false;
	});

	$(".main-menu a.calendarButton").click(function(){
			$("#menu-container .calendario-section").slideDown('slow');
			$("#calendar").fullCalendar("render");
			return false;
	});

	$(".main-menu a.profiloDipButton").click(function(){
			$(".profiloDip-section").load("static/templates/profiloDip.html #container-profiloDip");
			//$("#menu-container .content").slideUp('slow');
			$("#menu-container .profiloDip-section").slideDown('slow');

			$.getScript("static/js/modificaProfilo.js");

			return false;
	});


	$('#calendar').fullCalendar({
	      header: {
	        left: 'prev,next today',
	        center: 'title',
	        right: 'month,agendaWeek,agendaDay,listWeek'
	      },
	      defaultDate: '2018-02-12',
	      navLinks: true, // can click day/week names to navigate views
	      editable: true,
	      eventLimit: true, // allow "more" link when too many events
	      events: [
	        {
	          title: 'All Day Event',
	          start: '2018-02-01',
	        },
	        {
	          title: 'Long Event',
	          start: '2018-02-07',
	          end: '2018-02-10'
	        },
	        {
	          id: 999,
	          title: 'Repeating Event',
	          start: '2018-02-09T16:00:00'
	        },
	        {
	          id: 999,
	          title: 'Repeating Event',
	          start: '2018-02-16T16:00:00'
	        },
	        {
	          title: 'Conference',
	          start: '2018-02-11',
	          end: '2018-02-13'
	        },
	        {
	          title: 'Meeting',
	          start: '2018-02-12T10:30:00',
	          end: '2018-02-12T12:30:00'
	        },
	        {
	          title: 'Lunch',
	          start: '2018-02-12T12:00:00'
	        },
	        {
	          title: 'Meeting',
	          start: '2018-02-12T14:30:00'
	        },
	        {
	          title: 'Happy Hour',
	          start: '2018-02-12T17:30:00'
	        },
	        {
	          title: 'Dinner',
	          start: '2018-02-12T20:00:00'
	        },
	        {
	          title: 'Birthday Party',
	          start: '2018-02-13T07:00:00'
	        },
	        {
	          title: 'Click for Google',
	          url: 'http://google.com/',
	          start: '2018-02-28'
	        }
	      ]
	    });

})(jQuery);
