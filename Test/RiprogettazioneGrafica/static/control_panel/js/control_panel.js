class Control_panel extends OggettoBase {

    constructor(oggettoGeneratore, $where_to_append, $icon_position){
        super($('<div id="control-panel"> \
                    <div id="header-section" class="section-control-panel"> \
                        <div id="control-panel-foto-dip"><img id="foto-dip" src="static/img/nicola_pancheri.jpg"></div> \
                        <div id="control-panel-nome-dip"><label>Nicola Pancheri</label></div> \
                    </div> \
                    <div id="content-section" class="section-control-panel"> \
                        <ul> \
                            <li class="option-control_panel"> \
                                <a class="fa fa-user"><i>Pagina Profilo</i></a> \
                            </li> \
                            <li id="databases-list-control-panel" class="option-control_panel options-li navbar-toggler" data-toggle="collapse" data-target="#navbarNavDropdowndDatabase" aria-controls="navbarNavDropdowndDatabase" aria-expanded="false" aria-label="Toggle navigation database"> \
                                <a class="fa fa-database opzione-estentibile"><i>Database</i></a> \
                                <a id="extends-database-options" class="fa fa-plus"></a> \
                                <div class="collapse navbar-collapse" id="navbarNavDropdowndDatabase"> \
                                    <ul class="navbar-nav databases-list"> \
                                        <li class="nav-item prezzario-option active"> \
                                            <a class="nav-link" href="#">Prezzario Edile</a> \
                                        </li> \
                                        <li class="nav-item prezzario-option"> \
                                            <a class="nav-link" href="#">Prezzario Prodotti</a> \
                                        </li> \
                                        <li class="nav-item prezzario-option"> \
                                            <a class="nav-link" href="#">Scheda Fornitori</a> \
                                        </li> \
                                        <li class="nav-item prezzario-option"> \
                                            <a class="nav-link" href="#">Scheda Artigiani</a> \
                                        </li> \
                                    </ul> \
                                </div> \
                            <li class="option-control_panel"> \
                                <a class="fa fa-sign-out"><i>Logout</i></a> \
                            </li> \
                        </ul> \
                    </div> \
                  </div>'), oggettoGeneratore, $where_to_append );

        this.icon = $('<a class="nav-link headerItem fa fa-angle-double-left"></a>');
        this.$li_element = $('#databases-list-control-panel');
        this.$dropdown_elment = $('#navbarNavDropdowndDatabase');
        this.width = 305;


        this.icon.appendTo($icon_position);

        var thisRef = this;
        this.$li_element.click(function(){
            thisRef.sistemaVisualizzazioneDropdownListDatabase(thisRef);
        });

        /*nascondo il pannello e gli do l'effetto spostamento alla comparsa e all'uscita */
        this.referenzaDOM.css({'right': '-'+this.width+'px'});


        this.icon.click(function(){
            if($(this).hasClass('fa-angle-double-left')){
                $('#control-panel').animate({'right': '+='+thisRef.width+'px'});
                $(this).removeClass('fa-angle-double-left');
                $(this).addClass('fa-angle-double-right');

            }
            else{
                $('#control-panel').animate({'right': '-='+thisRef.width+'px'});
                $(this).removeClass('fa-angle-double-right');
                $(this).addClass('fa-angle-double-left');

            }


        });


    }

    sistemaVisualizzazioneDropdownListDatabase(thisRef){


        if(!thisRef.$dropdown_elment.hasClass('show')){
            thisRef.$li_element.css('height', 'unset');
            thisRef.$li_element.children('a.fa-plus').addClass('fa-minus');
            thisRef.$li_element.children('a.fa-minus').removeClass('fa-plus');

        }
        else{
            thisRef.$li_element.css('height', '50px');
            thisRef.$li_element.children('a.fa-minus').addClass('fa-plus');
            thisRef.$li_element.children('a.fa-plus').removeClass('fa-minus');
        }
    }
}