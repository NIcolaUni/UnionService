(function($) {

  $("#modificaProfiloButton").click(function(){
      console.log("Bella")
      $("#container-profiloDip").remove();
      $(".registraDip-section").load("static/templates/completaProfilo.html #container-contact100");
      $("#menu-container .content").slideUp('slow');
      $("#menu-container .registraDip-section").slideDown('slow');

      $.getScript("static/form/js/main.js");
      return false;
  });

})(jQuery);
