
var $li_element = $('#databases-list-control-panel');
var $dropdown_elment = $('#navbarNavDropdowndDatabase');
var sistemaVisualizzazioneDropdownList = function(){
        if(!$dropdown_elment.hasClass('show')){
            $li_element.css('height', 'unset');
            $li_element.children('a.fa-plus').addClass('fa-minus');
            $li_element.children('a.fa-minus').removeClass('fa-plus');

        }
        else{
            $li_element.css('height', '50px');
            $li_element.children('a.fa-minus').addClass('fa-plus');
            $li_element.children('a.fa-plus').removeClass('fa-minus');
        }


}

$(function(){

    $li_element.click(sistemaVisualizzazioneDropdownList);
});
