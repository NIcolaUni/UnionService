(function($) {



	$('.toggle-menu').click(function(){
        $('.show-menu').stop(true,true).slideToggle();
        return false;
  });


	$('.show-menu a').click(function() {
    	$('.show-menu').fadeOut('slow');
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
