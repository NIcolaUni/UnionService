(function($) {

/**
 * Header
 */

var header_main =  $('header'),
    toggle_search = $('.search-btn'),
    close_search = $('.searchbar__close'),
    toggleMenu = $('.header-menu__toggle'),
    headerMenu = $('.header-01__menu');

header_main.toggleClass("search-active");

toggle_search.on('click', function(){
    header_main.toggleClass("search-active");
});

close_search.on('click', function(){
    header_main.removeClass("search-active");
});

$('.searchbar__close').on('click', function(e) {
    e.stopPropagation();
});



})(jQuery);
