class Accogli_clientePage extends ActivityPage {

    constructor(oggettoGeneratore, $where_to_append, attivo, id_in_slider){
        super($('<div id="accogli_cliente_activity_container" class="activity_container"> \
                    <div id="accogli_cliente_space"> \
                        <div id="accogli_cliente_title"><div id="new_cliente_image_container"><img src="static/img/new-cliente.png"></img></div><label>Accoglienza cliente</label></div> \
                        <div id="accogli_cliente_form_space"> \
                            <div id="accogli_cliente_forms_container"> \
                                <label>ANAGRAFICA</label> \
                                <div id="nome_form"> \
                                        <input id="nome_cliente_input" type="text" placeholder="Nome cliente...">  \
                                        <input id="cognome_cliente_input" type="text" placeholder="Cognome cliente...">  \
                                </div> \
                                <div id="addr_form"> \
                                       <input id="via_cliente_input" type="text" placeholder="Via..."> \
                                        <input id="civico_cliente_input" type="number" placeholder="Civico...">  \
                                        <input id="cap_cliente_input" type="number" placeholder="CAP...">   \
                                        <select id="regione_select"><option>lombardia</option></select> \
                                </div> \
                                <label>CONTATTI</label> \
                                <div id="contatti_form"> \
                                        <input id="telefono_cliente_input" type="telephone" placeholder="Telefono...">  \
                                        <input id="email_cliente_input" type="email" placeholder="Email...">  \
                                </div> \
                                <label>LAVORAZIONE</label> \
                                <div id="lavorazione_form"> \
                                    <textarea id="lavorazione_textarea"></textarea> \
                                </div> \
                                <label>INFO EXTRA</label> \
                                <div id="info_extra_form"> \
                                </div> \
                            </div> \
                        </div> \
                    </div> \
                 </div>'),
                    oggettoGeneratore, $where_to_append, attivo, id_in_slider);

        $('#accogli_cliente_forms_container input').hover(function(){$(this).focus()});
        $('#accogli_cliente_forms_container select').hover(function(){$(this).focus()});
        $('#accogli_cliente_forms_container textarea').hover(function(){$(this).focus()});
    }
}