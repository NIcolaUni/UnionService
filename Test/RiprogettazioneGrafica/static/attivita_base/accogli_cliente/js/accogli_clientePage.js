class Accogli_clientePage extends ActivityPage {

    constructor(oggettoGeneratore, $where_to_append, attivo, id_in_slider){
        super($('<div id="accogli_cliente_activity_container" class="activity_container"> \
                    <div id="accogli_cliente_space"> \
                        <div id="accogli_cliente_title"><div id="new_cliente_image_container"><img src="static/img/new-cliente.png"></img></div><label>Accoglienza cliente</label></div> \
                        <div id="accogli_cliente_form_space"> \
                            <div id="accogli_cliente_forms_container"> \
                                <form id="accogli_cliente_form_nome " class="form_container" > \
                                    <input id="nome_cliente_input" type="text" placeholder="Nome cliente...">  \
                                    <input id="cognome_cliente_input" type="text" placeholder="Cognome cliente...">  \
                                </form> \
                                <form id="accogli_cliente_form_addr" class="form_container" > \
                                    <div><input id="via_cliente_input" type="text" placeholder="Via cliente..."></div>  \
                                    <div><input id="civico_cliente_input" type="number" placeholder="Civico cliente..."></div>   \
                                    <div><input id="cap_cliente_input" type="number" placeholder="CAP..."></div>   \
                                    <div><select id="regione_select"><option>lombardia</option></select></div>  \
                                </form> \
                            </div> \
                        </div> \
                    </div> \
                 </div>'),
                    oggettoGeneratore, $where_to_append, attivo, id_in_slider);
    }
}