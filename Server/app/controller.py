from flask import render_template, redirect, request, url_for, session, request, send_from_directory
from app import server, socketio, accoglienzaForm
from .model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm, ClienteAccoltoForm, ApriPaginaClienteForm, AggiungiFornitoreForm
from .model.dipendenteFittizio import DipendenteFittizio
from .model.dipendenteRegistrato import DipendenteRegistrato
from .model.dipendente import Dipendente
from .model.notifica import Notifica
from .model.settoreLavorazione import SettoreLavorazione
from .model.prezzarioEdile import PrezzarioEdile
from .model.clienteAccolto import ClienteAccolto
from .model.impegni import Impegni
from .model.fornitore import Fornitore
from .model.sottoGruppoFornitori import SottoGruppoFornitori
from .model.rappresentate import Rappresentante
from .model.tipologiaProdotto import TipologiaProdotto
from .model.modelloProdotto import ModelloProdotto
from .model.prodottoPrezzario import ProdottoPrezzario
from .model.giorniPagamentoFornitore import GiorniPagamentoFornitore
from .model.modalitaPagamentoFornitore import ModalitaPagamentoFornitore
from .model.tipologiaPagamentoFornitore import TipologiaPagamentoFornitore
from .model.preventivoEdile import PreventivoEdile
from .model.preventivoFiniture import PreventivoFiniture
from .model.eccezioni.righaPresenteException import RigaPresenteException
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import emit, join_room, leave_room
import app
import json


####################################### ROUTE HANDLER #################################################

@server.route('/prezzarioEdile')
@login_required
def prezzarioEdile():
    #server.logger.info("\n\nchiamato {}\n\n".format(app.prezzarioEdileSettoreCorrente))
    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    settori = SettoreLavorazione.query.all()
    #categorie = Categoria.query.all()
   # pertinenze = Pertinenza.query.all()
    lavorazioni = PrezzarioEdile.query.all()

    if app.prezzarioEdileSettoreCorrente is None:
        if len(lavorazioni) != 0:
            app.prezzarioEdileSettoreCorrente = lavorazioni[0].settore

    if app.prezzarioEdileSettoreCorrente is not None:

        #server.logger.info("\n\nchiamato {} {} {}\n\n".format(settori, categorie, pertinenze))
        return render_template('prezzarioEdile.html', dipendente=dip, settori=settori, settoreToSel=app.prezzarioEdileSettoreCorrente,
                                        lavorazioni=lavorazioni,
                                        sockUrl=app.appUrl, prezzario=True, prezzarioEdileCss=True)
    else:
        return render_template('prezzarioEdile.html', dipendente=dip, settori=settori, settoreToSel=None,
                                        lavorazioni=lavorazioni,
                                        sockUrl=app.appUrl, prezzario=True, prezzarioEdileCss=True)

@server.route('/prezzarioProdotti')
@login_required
def prezzarioProdotti():
    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    tipoProdotto = TipologiaProdotto.query.all()
    fornitori = SottoGruppoFornitori.query.all()
    prodotti =ProdottoPrezzario.query.all()
    modelli = ModelloProdotto.query.all()

    if app.prezzarioProdottiTipoCorrente is None:
        if len(tipoProdotto) != 0:
            app.prezzarioProdottiTipoCorrente = tipoProdotto[0].nome

    allerta = False

    if app.rigaPresente:
        allerta = True
        app.rigaPresente = False

    if app.prezzarioEdileSettoreCorrente is not None:

        return render_template('modificaPrezzarioProdotti.html', dipendente=dip, rigaPresente=allerta, tabellaRigaPresente=app.tabellaRigaPresente,
                               tipoProdotto=tipoProdotto, tipoToSel=app.prezzarioProdottiTipoCorrente, modelli=modelli,
                                fornitori=fornitori, prodotti=prodotti, prezzario=True, prezzarioProdottiCss=True, sockUrl=app.appUrl )
    else:
        return render_template('modificaPrezzarioProdotti.html', dipendente=dip, rigaPresente=allerta, tabellaRigaPresente=app.tabellaRigaPresente,
                                tipoProdotto=tipoProdotto, tipoToSel=None, prodotti=prodotti, modelli=modelli,
                                fornitori=fornitori, prezzario=True, prezzarioProdottiCss=True, sockUrl=app.appUrl )

@server.route('/schedaFornitori', methods=['GET', 'POST'])
@login_required
def schedaFornitori():

    form = AggiungiFornitoreForm(request.form)
    errorVar = False
    errorMessage = ""

    if request.method == 'POST':
    #registrazione nuovo fornitore
        server.logger.info("\n\nEntrato in Post {}\n\n".format(form.gruppo_azienda.data))

        #se non viene inserito nemmeno il nome del primo gruppo
        #la registrazione abortisce
        if form.gruppo_azienda.data == '':
            dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
            fornitori_primo_gruppo = Fornitore.query.order_by(Fornitore.nome_gruppo).all()
            fornitori_sotto_gruppo = SottoGruppoFornitori.query.order_by(SottoGruppoFornitori.nome).all()
            listaRappresentanti = Rappresentante.query.order_by(Rappresentante.nome).all()
            giorniPagamento = GiorniPagamentoFornitore.query.order_by(GiorniPagamentoFornitore.nome).all()
            modalitaPagamento = ModalitaPagamentoFornitore.query.order_by(ModalitaPagamentoFornitore.nome).all()
            tipologiaPagamento = TipologiaPagamentoFornitore.query.order_by(TipologiaPagamentoFornitore.nome).all()


            return render_template("schedaFornitori-rifatta.html", dipendente=dip,
                                   schedaFornitoriCss=True,
                                   giorniPagamento=giorniPagamento, modalitaPagamento=modalitaPagamento,
                                   listaFornitoriPrimoGruppo=fornitori_primo_gruppo,
                                   listaFornitoriSottoGruppo=fornitori_sotto_gruppo,
                                   listaRappresentanti=listaRappresentanti,
                                   tipologiaPagamento=tipologiaPagamento, form=form, sockUrl=app.appUrl, error=True, errorMessage="Inserire almeno il nome del primo gruppo")

        fornitore = Fornitore.query.filter_by(nome_gruppo=form.gruppo_azienda.data).first()

        #registro fornitore ovvero primo gruppo solo se non e' gia registrato
        if fornitore is not None:
            if not fornitore.has_sottoGruppo:
                Fornitore.setHas_sottoGruppi(fornitore=form.gruppo_azienda.data, value=True)
        else:
            try:
                Fornitore.registraFornitore(nome_gruppo=form.gruppo_azienda.data, has_sottoGruppo=True)
            except RigaPresenteException as e:
                server.logger.info("\n\n\n\n {} ".format(e))

        GiorniPagamentoFornitore.registraGiorniPagamento(nome=form.giorniPagamenti.data)
        ModalitaPagamentoFornitore.registraModalitaPagamento(nome=form.modalitaPagamenti.data)
        TipologiaPagamentoFornitore.registraTipologiaPagamento(nome=form.tipologiaPagamenti.data)

        #registro sottogruppo
        try:
            SottoGruppoFornitori.registraSottoGruppoFornitori(nome=form.nomeFornitore.data,
                                                              gruppo_azienda=form.gruppo_azienda.data,
                                                              settoreMerceologico=form.settoreMerceologico.data,
                                                              stato=form.stato.data,
                                                              tempiDiConsegna=form.tempiDiConsegna.data,
                                                              prezziNetti=form.prezziNetti.data,
                                                              scontoStandard=form.scontoStandard.data,
                                                              scontoExtra1=form.scontoExtra1.data,
                                                              scontroExtra2=form.scontroExtra2.data,
                                                              trasporto=form.trasporto.data,
                                                              imballo=form.imballo.data,
                                                              montaggio=form.montaggio.data,
                                                              trasportoUnitaMisura=form.trasportoUnitaMisura.data,
                                                              imballoUnitaMisura=form.imballoUnitaMisura.data,
                                                              montaggioUnitaMisura=form.montaggioUnitaMisura.data,
                                                              giorniPagamenti=form.giorniPagamenti.data,
                                                              modalitaPagamenti=form.modalitaPagamenti.data,
                                                              tipologiaPagamenti=form.tipologiaPagamenti.data,
                                                              provincia=form.provincia.data,
                                                              indirizzo=form.indirizzo.data,
                                                              telefono=form.telefono.data,
                                                              sito=form.sito.data)

        except RigaPresenteException as e:
            server.logger.info("\n\n\n\n {} ".format(e))
            app.rigaPresente=True
            app.tabellaRigaPresente="Sottogruppo fornitori"

        #se e' stato specificato un rappresentate, lo registro.
        if form.nomeRappresentante.data != '' and form.nomeRappresentante.data != ' ':
            try:
                Rappresentante.registraRappresentante(nome=form.nomeRappresentante.data, azienda=form.gruppo_azienda.data,
                                                      telefono=form.telefonoRappresentante.data,
                                                      email=form.emailRappresentante.data)
            except RigaPresenteException as e:
                server.logger.info("\n\n\n\n {} ".format(e))
                errorVar =True
                errorMessage = "Fornitore già registrato"



    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    fornitori_primo_gruppo = Fornitore.query.order_by(Fornitore.nome_gruppo).all()
    fornitori_sotto_gruppo = SottoGruppoFornitori.query.order_by(SottoGruppoFornitori.nome).all()
    listaRappresentanti = Rappresentante.query.order_by(Rappresentante.nome).all()
    giorniPagamento = GiorniPagamentoFornitore.query.order_by(GiorniPagamentoFornitore.nome).all()
    modalitaPagamento = ModalitaPagamentoFornitore.query.order_by(ModalitaPagamentoFornitore.nome).all()
    tipologiaPagamento = TipologiaPagamentoFornitore.query.order_by(TipologiaPagamentoFornitore.nome).all()

    allerta = False

    if app.rigaPresente:
        allerta = True
        app.rigaPresente = False

    return render_template("schedaFornitori-rifatta.html", dipendente=dip,
                           rigaPresente=allerta, tabellaRigaPresente=app.tabellaRigaPresente, schedaFornitoriCss=True,
                           giorniPagamento=giorniPagamento, modalitaPagamento=modalitaPagamento,
                           listaFornitoriPrimoGruppo=fornitori_primo_gruppo,
                           listaFornitoriSottoGruppo=fornitori_sotto_gruppo, listaRappresentanti = listaRappresentanti,
                           tipologiaPagamento=tipologiaPagamento, form=form, error=errorVar, errorMessage=errorMessage, sockUrl=app.appUrl)


@server.route('/cancellaFornitore/<nomeFornitore>/<primoGruppo>', methods=['GET', 'POST'])
@login_required
def cancellaFornitore(nomeFornitore, primoGruppo):

    if nomeFornitore == 'spazio':
        nomeFornitore = ''


    SottoGruppoFornitori.eliminaSottoGruppoFornitori(nome=nomeFornitore, gruppo_azienda=primoGruppo)
    return redirect("/schedaFornitori")

@server.route('/modificaFornitore/<nomeFornitore>/<primoGruppo>/<nomeRappresentante>')
@login_required
def modificaFornitore(nomeFornitore, primoGruppo, nomeRappresentante):

    if nomeFornitore == 'spazio':
        nomeFornitore = ''

    if nomeRappresentante == 'spazio':
        nomeRappresentante = ''

    form = AggiungiFornitoreForm(request.form)
    errorVar = False
    errorMessage = ""

    if request.method == 'POST':
    #modifica fornitore
        server.logger.info("\n\nEntrato in Post {}\n\n".format(form.gruppo_azienda.data))

        #se non viene inserito nemmeno il nome del primo gruppo
        #la registrazione abortisce
        if form.gruppo_azienda.data == '':
            dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
            fornitori_primo_gruppo = Fornitore.query.order_by(Fornitore.nome_gruppo).all()
            fornitori_sotto_gruppo = SottoGruppoFornitori.query.filter_by(nome=nomeFornitore).first()
            listaRappresentanti = Rappresentante.query.order_by(Rappresentante.nome).all()
            giorniPagamento = GiorniPagamentoFornitore.query.order_by(GiorniPagamentoFornitore.nome).all()
            modalitaPagamento = ModalitaPagamentoFornitore.query.order_by(ModalitaPagamentoFornitore.nome).all()
            tipologiaPagamento = TipologiaPagamentoFornitore.query.order_by(TipologiaPagamentoFornitore.nome).all()


            return render_template("modificaFornitore.html", dipendente=dip,
                                   schedaFornitoriCss=True,
                                   giorniPagamento=giorniPagamento, modalitaPagamento=modalitaPagamento,
                                   listaFornitoriPrimoGruppo=fornitori_primo_gruppo,
                                   sottoGruppoSelected=fornitori_sotto_gruppo,
                                   listaRappresentanti=listaRappresentanti,
                                   tipologiaPagamento=tipologiaPagamento, form=form, sockUrl=app.appUrl, error=True, errorMessage="Non è stato inserito alcun primo gruppo")

        fornitore = Fornitore.query.filter_by(nome_gruppo=form.gruppo_azienda.data).first()

        #registro fornitore ovvero primo gruppo solo se non e' gia registrato
        if fornitore is not None:
            if not fornitore.has_sottoGruppo:
                Fornitore.setHas_sottoGruppi(fornitore=form.gruppo_azienda.data, value=True)
        #se il fornitore e' cambiato e non esiste ancora
        else:
            try:
                Fornitore.registraFornitore(nome_gruppo=form.gruppo_azienda.data, has_sottoGruppo=True)
            except RigaPresenteException as e:
                server.logger.info("\n\n\n\n {} ".format(e))

        GiorniPagamentoFornitore.registraGiorniPagamento(nome=form.giorniPagamenti.data)
        ModalitaPagamentoFornitore.registraModalitaPagamento(nome=form.modalitaPagamenti.data)
        TipologiaPagamentoFornitore.registraTipologiaPagamento(nome=form.tipologiaPagamenti.data)

        #modifico sottogruppo
        try:
            SottoGruppoFornitori.modificaSottoGruppoFornitori(nome=form.nomeFornitore.data,
                                                              gruppo_azienda=form.gruppo_azienda.data,
                                                              settoreMerceologico=form.settoreMerceologico.data,
                                                              stato=form.stato.data,
                                                              tempiDiConsegna=form.tempiDiConsegna.data,
                                                              prezziNetti=form.prezziNetti.data,
                                                              scontoStandard=form.scontoStandard.data,
                                                              scontoExtra1=form.scontoExtra1.data,
                                                              scontroExtra2=form.scontroExtra2.data,
                                                              trasporto=form.trasporto.data,
                                                              trasportoUnitaMisura=form.trasportoUnitaMisura.data,
                                                              giorniPagamenti=form.giorniPagamenti.data,
                                                              modalitaPagamenti=form.modalitaPagamenti.data,
                                                              tipologiaPagamenti=form.tipologiaPagamenti.data,
                                                              provincia=form.provincia.data,
                                                              indirizzo=form.indirizzo.data,
                                                              telefono=form.telefono.data,
                                                              sito=form.sito.data)

        except RigaPresenteException as e:
            server.logger.info("\n\n\n\n {} ".format(e))
            app.rigaPresente=True
            app.tabellaRigaPresente="Sottogruppo fornitori"

        #se e' stato specificato un rappresentate, lo modifico.
        if form.nomeRappresentante.data != '' and form.nomeRappresentante.data != ' ':
            try:
                Rappresentante.modificaRappresentante(oldNome=nomeRappresentante, nome=form.nomeRappresentante.data,
                                                      azienda=form.gruppo_azienda.data,
                                                      telefono=form.telefonoRappresentante.data,
                                                      email=form.emailRappresentante.data)
            except RigaPresenteException as e:
                server.logger.info("\n\n\n\n {} ".format(e))
                errorVar =True
                errorMessage = "Rappresentante già registrato"



    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    fornitori_primo_gruppo = Fornitore.query.order_by(Fornitore.nome_gruppo).all()
    fornitori_sotto_gruppo = SottoGruppoFornitori.query.filter_by(nome=nomeFornitore).first()
    listaRappresentanti = Rappresentante.query.order_by(Rappresentante.nome).all()
    giorniPagamento = GiorniPagamentoFornitore.query.order_by(GiorniPagamentoFornitore.nome).all()
    modalitaPagamento = ModalitaPagamentoFornitore.query.order_by(ModalitaPagamentoFornitore.nome).all()
    tipologiaPagamento = TipologiaPagamentoFornitore.query.order_by(TipologiaPagamentoFornitore.nome).all()

    allerta = False

    if app.rigaPresente:
        allerta = True
        app.rigaPresente = False

    return render_template("modificaFornitore.html", dipendente=dip,
                           rigaPresente=allerta, tabellaRigaPresente=app.tabellaRigaPresente, schedaFornitoriCss=True,
                           giorniPagamento=giorniPagamento, modalitaPagamento=modalitaPagamento,
                           listaFornitoriPrimoGruppo=fornitori_primo_gruppo,
                           sottoGruppoSelected=fornitori_sotto_gruppo, listaRappresentanti = listaRappresentanti,
                           tipologiaPagamento=tipologiaPagamento, form=form, error=errorVar, errorMessage=errorMessage, sockUrl=app.appUrl)





@server.route('/gestioneDip', methods=['GET','POST'])
@login_required
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():

        DipendenteFittizio.registraDipendente(username=form.username.data, password=form.password.data,
                                                classe=form.tipo_dip.data, dirigente=form.dirigente.data, creatoreCredenziali=current_user.get_id())

        return redirect('/homepage')
    else:
        form.assegnaUserEPass()
        return render_template('gestioneDip.html', form=form )

@server.route('/paginaProfilo')
@login_required
def paginaProfilo():
    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('paginaProfilo.html', dipendente=dip)


@server.route('/newPreventivoEdile')
@login_required
def newPreventivoEdile():
    settori = SettoreLavorazione.query.all()
    prezzarioEdile = PrezzarioEdile.query.all()
    preventivo = PreventivoEdile.query.filter_by(numero_preventivo=app.preventivoEdileSelezionato[0], data=app.preventivoEdileSelezionato[1]).first()
    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()

    return render_template('preventivoEdile.html', codicePreventivo=codicePreventivo, settori=settori,
                            preventivoFullPage=True, cliente=cliente, prezzarioEdile=prezzarioEdile, preventivo=preventivo)


@server.route('/apriPreventivoEdile')
@login_required
def apriPreventivoEdile():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    settori = SettoreLavorazione.query.all()
    prezzarioEdile = PrezzarioEdile.query.all()
    preventivo = PreventivoEdile.query.filter_by(numero_preventivo=app.preventivoEdileSelezionato[0], data=app.preventivoEdileSelezionato[1]).first()
    infoPreventivo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=app.preventivoEdileSelezionato[0], data=app.preventivoEdileSelezionato[1])
    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()

    return render_template('preventivoEdile.html', codicePreventivo=codicePreventivo, settori=settori,
                            preventivoFullPage=True, cliente=cliente, prezzarioEdile=prezzarioEdile,
                            preventivo=preventivo, infoPreventivo=infoPreventivo, dipendente=dip)

@server.route('/downloadPreventivoEdile')
@login_required
def downloadPreventivoEdile():
    return send_from_directory(directory='preventiviLatexDir', filename='preventivo.pdf')


@server.route('/apriPreventivoFiniture')
@login_required
def apriPreventivoFiniture():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    tipologie = TipologiaProdotto.query.all()
    prezzarioProdotti = ProdottoPrezzario.query.all()
    modelliProdotto = ModelloProdotto.query.all()

    preventivo = PreventivoFiniture.query.filter_by(numero_preventivo=app.preventivoFinitureSelezionato[0], data=app.preventivoFinitureSelezionato[1]).first()
    #infoPreventivo = PreventivoFiniture.returnSinglePreventivo(numero_preventivo=app.preventivoFinitureSelezionato[0], data=app.preventivoFinitureSelezionato[1])
    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()

    return render_template('preventivoFiniture.html', codicePreventivo=codicePreventivo, tipologie=tipologie,
                            modelliProdotto=modelliProdotto,
                            preventivoFullPage=True, cliente=cliente, prezzarioProdotti=prezzarioProdotti,
                            preventivo=preventivo, dipendente=dip)

@server.route('/apriPaginaCliente', methods=['POST'])
@login_required
def apriPaginaCliente():
    '''
    Distinzione variabili "preventivi" e "preventivi_distinti" ritornate con la pagina:
    - preventivi: lista ordinata ( dalla data piu' recente alla piu' vecchia ) di preventivi
                    associati ad un dato cliente;

    - preventivi_distinti:  lista ordinata ( dalla data piu' recente alla piu' vecchia ) di preventivi
                                che differiscono soltanto nell'attributo "numero_preventivo";
    '''

    app.formCercaCliente = ApriPaginaClienteForm(request.form)
    scelta = app.formCercaCliente.nome_cognome_indirizzo.data
    (cognomeCliente, nomeCliente, indirizzoCliente) = scelta.split(" . ")
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    app.clienteSelezionato = ClienteAccolto.query.filter_by(nome=nomeCliente, cognome=cognomeCliente, indirizzo=indirizzoCliente).first()

    if app.clienteSelezionato is None:
        return redirect('/homepage')

    ufficioCommerciale = []#Dipendente.query.filter_by( classe="commerciale", username=cliente.commerciale )
    ufficioTecnico = []#Dipendente.query.filter_by( classe="tecnico", username=cliente.tecnico )
    ufficioCapicantiere = []#Dipendente.query.filter_by( classe="commerciale", username=cliente.capocantiere )


    return render_template('paginaCliente.html', dipendente=dip, cliente=app.clienteSelezionato, ufficioCommerciale=ufficioCommerciale,
                                                    ufficioTecnico=ufficioTecnico, ufficioCapicantiere=ufficioCapicantiere )

@server.route('/clientBack')
@login_required
def clientBack():

    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    ufficioCommerciale = []#Dipendente.query.filter_by( classe="commerciale", username=cliente.commerciale )
    ufficioTecnico = []#Dipendente.query.filter_by( classe="tecnico", username=cliente.tecnico )
    ufficioCapicantiere = []#Dipendente.query.filter_by( classe="commerciale", username=cliente.capocantiere )

    return render_template('paginaCliente.html', dipendente=dip, cliente=app.clienteSelezionato, ufficioCommerciale=ufficioCommerciale,
                            ufficioTecnico=ufficioTecnico, ufficioCapicantiere=ufficioCapicantiere)

@server.route('/anteprimaPreventivoEdile')
@login_required
def anteprimaPreventivoEdile():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()


    preventivi = PreventivoEdile.returnAllPreventiviCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    preventivi_distinti = []

    for preventivo in preventivi:
        preventivo_presente = False
        for prev_dist in preventivi_distinti:
            if preventivo[0].numero_preventivo == prev_dist[2]:
                preventivo_presente = True

        if not preventivo_presente:
            preventivi_distinti.append((preventivo[0].tipologia_commessa, preventivo[0].calcolaCodicePreventivo(),
                                        preventivo[0].numero_preventivo))

    lastPrev = PreventivoEdile.returnLastPreventivoCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    countPreventivi = PreventivoEdile.get_counter_preventivi_per_cliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    app.server.logger.info('elenco calcolo preventiviDistinti: {}'.format( preventivi_distinti ));
    return render_template('paginaCliente_prevEdile.html', dipendente=dip, cliente=app.clienteSelezionato,
                           preventivi=preventivi, preventivi_distinti=preventivi_distinti,
                           lastPreventivo=lastPrev, countPreventivi=countPreventivi)

@server.route('/anteprimaPreventivoFiniture')
@login_required
def anteprimaPreventivoFiniture():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()



    return render_template('paginaCliente_prevFiniture.html', dipendente=dip, cliente=app.clienteSelezionato, countPreventivi=0)


@server.route('/accoglienza/<int:error>', methods=['GET','POST'])
@login_required
def accoglienza(error):
    '''
    :param error:
    :return:
    '''

    '''
    Questo if è necessario poichè, al ritorno di una pagina per form non valido,
    la variabile accoglienzaForm viene sovrascritta con un form nuovo, ovvero quello
    richiamato dalla pagina stessa ritornata.
    '''
    if error == 1 :
        if app.accoglienzaOk:
            app.accoglienzaOk=False
            return render_template('confermaRegistrazioneCliente.html')
        else:
            return render_template('accoglienzaCliente.html', form=app.accoglienzaForm)

    app.accoglienzaForm = ClienteAccoltoForm(request.form)

    if request.method == 'POST':

        server.logger.info("\n\nEntrato in Post {}\n\n".format(app.accoglienzaForm))

        if app.accoglienzaForm.validate_on_submit():

            ClienteAccolto.registraCliente(nome=app.accoglienzaForm.nome.data, cognome=app.accoglienzaForm.cognome.data, indirizzo=app.app.accoglienzaForm.indirizzo.data,
                                           telefono=app.accoglienzaForm.telefono.data, email=app.accoglienzaForm.email.data, difficolta=app.accoglienzaForm.difficolta.data,
                                           tipologia=app.accoglienzaForm.tipologia.data, referenza=app.accoglienzaForm.referenza.data, sopraluogo=app.accoglienzaForm.sopraluogo.data,
                                           datasopraluogo=app.accoglienzaForm.datasopraluogo.data, lavorazione=app.accoglienzaForm.lavorazione.data, commerciale=current_user.get_id())

            app.accoglienzaOk=True
            return render_template('confermaRegistrazioneCliente.html')

    server.logger.info("\n\nAlternativa al post {}{}\n\n".format(app.accoglienzaForm.nome.errors, app.accoglienzaForm))

    return render_template('accoglienzaCliente.html', form=app.accoglienzaForm)



@server.route('/homepage')
@login_required
def homepage():

    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('homepage.html', dipendente=dip, sockUrl=app.appUrl)


@server.route('/impegni')
@login_required
def impegni():
    return render_template('impegni.html')

@server.route('/sidebarLeft')
@login_required
def sidebarLeft():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('sidebar-left.html', dipendente=dip)

@server.route('/header')
@login_required
def header():

    app.formCercaCliente = ApriPaginaClienteForm(request.form)

    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    listaClienti = []

    if dip.classe == 'commerciale':
        listaClienti = ClienteAccolto.query.filter_by(commerciale=current_user.get_id()).order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()

    elif dip.classe == 'commerciale':
        listaClienti = ClienteAccolto.query.filter_by(tecnico=current_user.get_id()).order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()

    elif dip.classe == 'capocantiere':
        listaClienti = ClienteAccolto.query.filter_by(capocantiere=current_user.get_id()).order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()



    numNot = Notifica.get_counter(dipendente=current_user.get_id())
    return render_template('header.html', numNotifiche=numNot, listaClienti=listaClienti, form=app.formCercaCliente)

@server.route('/registraDipendente', methods=['GET','POST'])
@login_required
def registraDipendente():
    form = RegistraDipendenteForm()

    if form.validate_on_submit():

        if Dipendente.query.filter_by(cf=form.cf.data).first() != None:
            return render_template("registrazioneDip.html", form=form, fittizio=True, errCf=True)

        domicilioDip = form.resEDomUguali.data

        if domicilioDip:
            domicilioDip = form.residenza.data
        else:
            domicilioDip = form.domicilio.data

        ( username, password, creatoreCredenziali ) = Dipendente.registraDipendente(dipFitUsername=current_user.get_id(), nome=form.nome.data, cognome=form.cognome.data,
                                cf=form.cf.data, dataNascita=form.dataNascita.data, residenza=form.residenza.data,
                                domicilio=domicilioDip, telefono=form.telefono.data,
                                password=form.password.data, email_aziendale=form.email_aziendale.data,
                                email_personale=form.email_personale.data, iban=form.iban.data, partitaIva=form.partitaIva.data )


        return render_template("confermaRegistrazione.html", username=username, password=password, creatoreCredenziali=creatoreCredenziali, sockUrl=app.appUrl )

    return render_template("registrazioneDip.html", form=form, fittizio=True)


@server.route('/', methods=['GET','POST'])
@server.route('/login', methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        dip=DipendenteRegistrato.query.filter_by(username=current_user.get_id()).first()
        if dip.fittizio:
            return redirect(url_for('registraDipendente'))
        return redirect(url_for('homepage'))

    form = LoginForm()


    if form.validate_on_submit():
        dip=DipendenteRegistrato.query.filter_by(username=form.username.data, password=form.password.data).first()
        if dip is None:
            return render_template("login.html", form=form, error="Credenziali errate!")

        login_user(dip, remember=True)


        return redirect(url_for('login'))

    return render_template("login.html", form=form)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@server.route('/getNotifiche')
@login_required
def getNotifiche():
    notiche = Notifica.query.filter_by(dipendente=current_user.get_id());

    returnList = ""

    for nota in notiche:
        returnList += '{ "titolo": "' +nota.titolo+ '", "contenuto": "' + nota.contenuto +'" },'

    return '{ "list":[' +returnList[:-1]+'] }'

@server.route('/listImpegni')
@login_required
def listImpegni():

    impegni = Impegni.query.filter_by(dipendente=current_user.get_id())

    return render_template('impegni.html', impegni=impegni)

@server.route('/getImpegni')
@login_required
def getImpegni():

    returnList = '{"todo": "sono un impegno difficile", "dirigente": "gianni"},'
    return '{ "list":[' +returnList[:-1]+'] }'

###########################################################################################################################################
########################################### SOCKETIO HANDLER ##############################################################################
###########################################################################################################################################

@socketio.on('my_event', namespace="/test")
def handle_my_event(message):
    server.logger.info('messagggio ricevuto: {}'.format(message['data']))
    #print('received message: ' + message)
    emit('my response', {'data': 'brao semo!'})

@socketio.on('registra_sid', namespace="/home")
def handle_registra_sid(message):
    Dipendente.registraSid(message['username'], request.sid)


@socketio.on('registrazione_effettuata', namespace="/notifica")
def handle_registrazione_effetuata(message):
    responsabile = Dipendente.query.filter_by(username=message['responsabile']).first()
    nuovoDip = Dipendente.query.filter_by(username=message['dipendente_registrato']).first()


    Notifica.registraNotifica(dipendente=responsabile.username, titolo="Aggiunto dipendente {0} {1}".format(nuovoDip.nome, nuovoDip.cognome),
                              contenuto="Ricorda di completare la sua registrazione.")

    emit('aggiornaNotifiche', {'titolo': "Aggiunto dipendente {0} {1}".format(nuovoDip.nome, nuovoDip.cognome),
                               'contenuto': "Ricorda di completare la sua registrazione."},
                                namespace='/notifica', room=responsabile.session_id)


@socketio.on('registra_settore', namespace="/prezzario")
def handle_registra_settore(message):

  #verifico che il settore non sia gia presente

  dip = Dipendente.query.filter_by(username=message['dip']).first()

  if SettoreLavorazione.query.filter_by(nome=message['settore'] ).first() is None:
      SettoreLavorazione.registraSettore(nome=message['settore'] )
      emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

  else:
      emit('abortAggiorna',  {'what': 'Settore'}, namespace='/prezzario', room=dip.session_id)


@socketio.on('elimina_settore', namespace="/prezzario")
def handle_elimina_settore(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    SettoreLavorazione.eliminaSettore(nome=message['settore'])
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

@socketio.on('registra_lavorazione', namespace="/prezzario")
def handle_registra_lavorazione(message):
    server.logger.info("\n\n\nWei sono il dip: {}\n\n\n".format(message['dip']))
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    PrezzarioEdile.registraLavorazione(settore=message["settore"], tipologia_lavorazione=message["tipologia"],
                                        pertinenza=message["pertinenza"], unitaMisura=message["unita"],
                                         costo=message["costo"], prezzoMin=message["pMin"], prezzoMax=message["pMax"],
                                          dimensione=message["dimensione"], fornitura=message["fornitura"], posa=message["posa"],
                                            note=message["note"])
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

@socketio.on('modifica_lavorazione', namespace="/prezzario")
def handle_modifica_lavorazione(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PrezzarioEdile.modificaLavorazione(settore=message["settore"], oldTipologia=message['oldTipologia'], tipologia_lavorazione=message["tipologia"],
                                        pertinenza=message["pertinenza"], unitaMisura=message["unita"],
                                         costo=message["costo"], prezzoMin=message["pMin"], prezzoMax=message["pMax"],
                                          dimensione=message["dimensione"], fornitura=message["fornitura"], posa=message["posa"],
                                            note=message["note"])

    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('cambia_settore_prezzario', namespace='/prezzario')
def handle_cambia_settore_prezzario(message):
    app.prezzarioEdileSettoreCorrente=message['settore']
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('setta_daVerificare', namespace='/prezzario')
def handle_setta_daVerificare(message):
    server.logger.info("\n\n\nMi è arrivato da registrare  {} {} {} \n\n\n".format(message['settore'], message['tipologia'], message['valore']))
    PrezzarioEdile.setDaVerificare(settore=message['settore'], tipologia_lavorazione=message['tipologia'], valore=message['valore'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)

@socketio.on('elimina_lavorazione', namespace='/prezzario')
def handle_elimina_lavorazione(message):
    PrezzarioEdile.eliminaLavorazione(settore=message['settore'], tipologia_lavorazione=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzario', room=dip.session_id)


@socketio.on('registraImpegno', namespace='/impegni')
def handle_registraImpegno(message):
    server.logger.info("Mi è arrivato da registrare per {}: {} ".format(message['dip'], message['testo']))

    if message['dir'] == "":
        Impegni.registraImpegni(dipendente=message['dip'], testo=message['testo'])
    else:
        Impegni.registraImpegni(dipendente=message['dip'], testo=message['testo'], dirigente=message['dir'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    emit('aggiornaImpegni', namespace='/impegni', room=dip.session_id)



@socketio.on('modifica_giornoPagamento', namespace="/fornitore")
def handle_modifica_giornoPagamento(message):
    GiorniPagamentoFornitore.modificaGiorniPagamento(newNome=message['newNome'], oldNome=message['oldNome'])

    listaGiorniPagamento = GiorniPagamentoFornitore.query.order_by(GiorniPagamentoFornitore.nome).all()
    newListToSend = dict()
    counter=0
    for giorno in listaGiorniPagamento:
        newListToSend[str(counter)]=giorno.nome
        counter+=1

    newListToSend['length']=counter

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaGiorniPagamento', newListToSend, namespace='/fornitore', room=dip.session_id)

@socketio.on('elimina_giornoPagamento', namespace="/fornitore")
def handle_elimina_giornoPagamento(message):
    GiorniPagamentoFornitore.eliminaGiorniPagamento(message['nome'])

    listaGiorniPagamento = GiorniPagamentoFornitore.query.order_by(GiorniPagamentoFornitore.nome).all()
    newListToSend = dict()
    counter=0
    for giorno in listaGiorniPagamento:
        newListToSend[str(counter)]=giorno.nome
        counter+=1

    newListToSend['length']=counter

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaGiorniPagamento', newListToSend, namespace='/fornitore', room=dip.session_id)

@socketio.on('modifica_modalitaPagamento', namespace="/fornitore")
def handle_modifica_modalitaPagamento(message):
    ModalitaPagamentoFornitore.modificaModalitaPagamento(newNome=message['newNome'], oldNome=message['oldNome'])

    listaModalitaPagamento = ModalitaPagamentoFornitore.query.order_by(ModalitaPagamentoFornitore.nome).all()
    newListToSend = dict()
    counter=0
    for giorno in listaModalitaPagamento:
        newListToSend[str(counter)]=giorno.nome
        counter+=1

    newListToSend['length']=counter

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaModalitaPagamento', newListToSend, namespace='/fornitore', room=dip.session_id)

@socketio.on('elimina_modalitaPagamento', namespace="/fornitore")
def handle_elimina_modalitaPagamento(message):
    ModalitaPagamentoFornitore.eliminaModalitaPagamento(message['nome'])

    listaModalitaPagamento = ModalitaPagamentoFornitore.query.order_by(ModalitaPagamentoFornitore.nome).all()
    newListToSend = dict()
    counter=0
    for giorno in listaModalitaPagamento:
        newListToSend[str(counter)]=giorno.nome
        counter+=1

    newListToSend['length']=counter

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaModalitaPagamento', newListToSend, namespace='/fornitore', room=dip.session_id)

@socketio.on('modifica_tipologiaPagamento', namespace="/fornitore")
def handle_modifica_tipologiaPagamento(message):
    TipologiaPagamentoFornitore.modificaTipologiaPagamento(newNome=message['newNome'], oldNome=message['oldNome'])

    listTipologiaPagamento = TipologiaPagamentoFornitore.query.order_by(TipologiaPagamentoFornitore.nome).all()
    newListToSend = dict()
    counter=0
    for giorno in listTipologiaPagamento:
        newListToSend[str(counter)]=giorno.nome
        counter+=1

    newListToSend['length']=counter

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaTipologiaPagamento', newListToSend, namespace='/fornitore', room=dip.session_id)

@socketio.on('elimina_tipologiaPagamento', namespace="/fornitore")
def handle_elimina_tipologiaPagamento(message):
    TipologiaPagamentoFornitore.eliminaTipologiaPagamento(message['nome'])

    listTipologiaPagamento = TipologiaPagamentoFornitore.query.order_by(TipologiaPagamentoFornitore.nome).all()
    newListToSend = dict()
    counter=0
    for giorno in listTipologiaPagamento:
        newListToSend[str(counter)]=giorno.nome
        counter+=1

    newListToSend['length']=counter

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaTipologiaPagamento', newListToSend, namespace='/fornitore', room=dip.session_id)



@socketio.on('registra_tipologiaProdotto', namespace="/prezzarioProdotti")
def handle_registra_tipologiaProdotto(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    try:
        TipologiaProdotto.registraTipologiaProdotto(nome=message['nomeTipo'])
    except RigaPresenteException as e:
        server.logger.info("\n\n\n\n {} ".format(e))
        app.rigaPresente=True
        app.tabellaRigaPresente="Tipologia prodotto"
     #   emit('waitForSwallClose', {"who": "Tipologia prodotto"}, namespace='/prezzarioProdotti', room=dip.session_id)


    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)

@socketio.on('cambia_tipologia_prezzario', namespace='/prezzarioProdotti')
def handle_cambia_settore_prezzario(message):
    app.prezzarioProdottiTipoCorrente = message['tipologia']

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)


@socketio.on('registra_prodotto', namespace='/prezzarioProdotti')
def handle_registra_prodotto(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()


    try:
        if message['capitolato']:
            ProdottoPrezzario.registraProdotto( nome=message['nome'], tipologia=message['tipologia'], capitolato=message['modello'])

        else:
            ProdottoPrezzario.registraProdotto(nome=message['nome'], tipologia=message['tipologia'])

        if message['versoDiLettura']:

                ModelloProdotto.registraModello(   nome=message['modello'],
                                                   prodotto=message['nome'], tipologia=message['tipologia'],
                                                   marchio=message['marchio'],
                                                   codice=message['codice'],

                                                   fornitore_primo_gruppo=message['fornitore_primo_gruppo'],
                                                   fornitore_sotto_gruppo=message['fornitore_sotto_gruppo'],

                                                   prezzoListinoFornitura=message['prezzoListinoFornitura'],
                                                   prezzoListinoFornituraPosa=message['prezzoListinoFornituraPosa'],
                                                   nettoUsFornituraPosa=message['nettoUsFornituraPosa'],
                                                   nettoUsFornitura=message['nettoUsFornitura'],
                                                   posa=message['posa'],
                                                   rincaroCliente=message['rincaroCliente'],
                                                   versoDiLettura=message['versoDiLettura'])

        else:
                ModelloProdotto.registraModello(   nome=message['modello'],
                                                   prodotto=message['nome'], tipologia=message['tipologia'],
                                                   marchio=message['marchio'],
                                                   codice=message['codice'],

                                                   fornitore_primo_gruppo=message['fornitore_primo_gruppo'],
                                                   fornitore_sotto_gruppo=message['fornitore_sotto_gruppo'],
                                                   prezzoListinoFornitura=message['prezzoListinoFornitura'],
                                                   prezzoListinoFornituraPosa=message['prezzoListinoFornituraPosa'],
                                                   rincaroAzienda=message['rincaroAzienda'],
                                                   trasportoAzienda=message['trasportoAzienda'],
                                                   imballoAzienda=message['imballoAzienda'],
                                                   posa=message['posa'],
                                                   nettoUsFornitura=message['nettoUsFornitura'],
                                                   nettoUsFornituraPosa=message['nettoUsFornituraPosa'],
                                                   rincaroCliente=message['rincaroCliente'],
                                                   versoDiLettura=message['versoDiLettura'])


    except  RigaPresenteException as e:
        server.logger.info("\n\n\n\n {} ".format(e))
        app.rigaPresente = True
        app.tabellaRigaPresente = "Prodotto"

    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)

@socketio.on('elimina_prodotto', namespace='/prezzarioProdotti')
def handle_elimina_prodotto(message):
    ProdottoPrezzario.eliminaProdotto(nome=message['prodotto'], tipologia=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)

@socketio.on('modifica_prodotto', namespace='/prezzarioProdotti')
def handle_modifica_prodotto(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()


    try:

        if message['versoDiLettura']:

                ProdottoPrezzario.modificaProdotto({ 'nome':message['nome'],
                                                     'oldNome': message['old_nome'],
                                                     'tipologia': message['tipologia'],
                                                   'marchio':message['marchio'],
                                                   'codice':message['codice'],
                                                    'modello' : message['modello'],
                                                   'fornitore_primo_gruppo':message['fornitore_primo_gruppo'],
                                                   'fornitore_sotto_gruppo':message['fornitore_sotto_gruppo'],
                                                   'prezzoListinoFornitura' :message['prezzoListinoFornitura'],
                                                   'prezzoListinoFornituraPosa' :message['prezzoListinoFornituraPosa'],
                                                   'posa' : message['posa'],
                                                   'nettoUsFornituraPosa':message['nettoUsFornituraPosa'],
                                                   'nettoUsFornitura':message['nettoUsFornitura'],
                                                   'rincaroCliente':message['rincaroCliente'],
                                                   'versoDiLettura':message['versoDiLettura']})

        else:
                ProdottoPrezzario.modificaProdotto(
                                                   {'nome': message['nome'],
                                                   'oldNome': message['old_nome'],
                                                   'tipologia': message['tipologia'],
                                                   'marchio': message['marchio'],
                                                   'codice': message['codice'],
                                                    'modello': message['modello'],
                                                   'fornitore_primo_gruppo': message['fornitore_primo_gruppo'],
                                                   'fornitore_sotto_gruppo': message['fornitore_sotto_gruppo'],
                                                   'prezzoListinoFornitura': message['prezzoListinoFornitura'],
                                                   'prezzoListinoFornituraPosa': message['prezzoListinoFornituraPosa'],
                                                   'rincaroAzienda': message['rincaroAzienda'],
                                                   'trasportoAzienda': message['trasportoAzienda'],
                                                   'imballoAzienda': message['imballoAzienda'],
                                                   'posa': message['posa'],
                                                   'nettoUsFornitura': message['nettoUsFornitura'],
                                                   'nettoUsFornituraPosa' : message['nettoUsFornituraPosa'],
                                                   'rincaroCliente': message['rincaroCliente'],
                                                   'versoDiLettura': message['versoDiLettura']})


    except  RigaPresenteException as e:
        server.logger.info("\n\n\n\n {} ".format(e))
        app.rigaPresente = True
        app.tabellaRigaPresente = "Prodotto"


    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)


@socketio.on('settaProdottoDaVerificare', namespace='/prezzarioProdotti')
def handle_settaProdottoDaVerificare(message):
    ProdottoPrezzario.setDaVerificare(tipologia=message['tipo'], nome=message['prodotto'], valore=message['valore'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)

@socketio.on('modifica_tipologia_prodotto', namespace='/prezzarioProdotti')
def handle_modifica_tipologia_prodotto(message):
    TipologiaProdotto.modificaTipologiaProdotto(nome=message['tipologia'], oldNome=message['oldTipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)

@socketio.on('elimina_tipologia_prodotto', namespace='/prezzarioProdotti')
def handle_elimina_tipologia_prodotto(message):
    TipologiaProdotto.eliminaTipologiaProdotto(message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)

@socketio.on('aggiungi_modello_prodotto', namespace='/prezzarioProdotti')
def handle_aggiungi_modello_prodotto(message):
    ModelloProdotto.registraModelloProdotto(nome=message['nome'], tipologia=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)


@socketio.on('registra_nuovo_preventivo', namespace='/preventivoFiniture')
def handle_registra_nuovo_preventivo(message):
    app.server.logger.info('\n\n\n\nEhi ciao prev finit \n\n\n\n')
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    idPreventivo = PreventivoFiniture.registraPreventivo(nome_cliente=message['nome_cliente'],
                                       cognome_cliente=message['cognome_cliente'], indirizzo_cliente=message['indirizzo_cliente'],
                                        dipendente_generatore=dip.username)

    app.preventivoFinitureSelezionato=idPreventivo
    emit('confermaRegistrazionePreventivo', namespace='/preventivoFiniture', room=dip.session_id)

@socketio.on('registra_nuovo_preventivo', namespace='/preventivoEdile')
def handle_registra_nuovo_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    idPreventivo = PreventivoEdile.registraPreventivo(nome_cliente=message['nome_cliente'],
                                       cognome_cliente=message['cognome_cliente'], indirizzo_cliente=message['indirizzo_cliente'],
                                        dipendente_generatore=dip.username, tipologia_commessa=message['tipologia_commessa'])

    app.preventivoEdileSelezionato=idPreventivo
    emit('confermaRegistrazionePreventivo', namespace='/preventivoEdile', room=dip.session_id)

@socketio.on('elimina_preventivo', namespace='/preventivoEdile')
def handle_elimina_preventivo(message):
    server.logger.info('Start elimina preventivo')
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    server.logger.info('Start elimina preventivo 1')

    PreventivoEdile.eliminaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'])

    server.logger.info('Start elimina preventivo 2')

    preventiviRestanti = PreventivoEdile.get_counter_preventivi_per_numero(numero_preventivo=message['numero_preventivo'])

    server.logger.info('Start elimina preventivo 3')

    emit('aggiornaAnteprimaPreventivoEdile',
                    {
                        'numero_preventivo_deleted' : message['numero_preventivo'],
                        'data_deleted' : message['data'],
                        'preventivi_restanti': preventiviRestanti

                    }, namespace='/preventivoEdile', room=dip.session_id)

@socketio.on('modifica_preventivo_edile', namespace='/preventivoEdile')
def handle_modifica_preventivo_edile(message):
    server.logger.info('\n\nModifica preventivo iniziato\n\n')
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    idPreventivo = PreventivoEdile.modificaPreventivo(numero_preventivo=message['numero_preventivo'], dipendente_ultimaModifica=dip)
    app.preventivoEdileSelezionato=idPreventivo
    server.logger.info('\n\nModifica preventivo iniziato: {}\n\n'.format(idPreventivo))

    emit('startModificaPreventivo', namespace='/preventivoEdile', room=dip.session_id)


@socketio.on('add_nuova_lavorazione', namespace='/preventivoEdile')
def handle_add_nuova_lavorazione(message):

    PreventivoEdile.registraLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                         ordine=message['ordine'], settore=message['settore'], tipologia_lavorazione=message['lavorazione'],
                                        numero=1, larghezza=1, altezza=1, profondita=1, unitaMisura=message['unitaMisura'],
                                        prezzoUnitario=message['prezzoUnitario'])

@socketio.on('elimina_lavorazione', namespace='/preventivoEdile')
def handle_elimina_lavorazione(message):
    PreventivoEdile.eliminaLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'], ordine=message['ordine'])

@socketio.on('modifica_ordine_lavorazione', namespace='/preventivoEdile')
def handle_modifica_ordine_lavorazione(message):

    PreventivoEdile.iniziaRiordinoLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'])

    PreventivoEdile.modificaOrdineLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                            ordine=int('-'+message['ordineVecchio']), modifica={'ordine' : message['ordineNuovo']})

@socketio.on('add_nuova_sottolavorazione', namespace='/preventivoEdile')
def handle_add_nuova_sottolavorazione(message):
    PreventivoEdile.nuovaSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                           ordine=message['ordine'])

@socketio.on('elimina_sottolavorazione', namespace='/preventivoEdile')
def handle_elimina_sottolavorazione(message):
    PreventivoEdile.eliminaSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                             ordine=message['ordine'], ordine_sottolavorazione=message['ordine_sottolavorazione'])

@socketio.on('modifica_ordine_sottolavorazione', namespace='/preventivoEdile')
def handle_modifica_ordine_sottolavorazione(message):

    server.logger.info('\n\n\n numero_preventivo:' +
                       message['numero_preventivo']+
                       '\n'+
                       'data: '+
                       message['data'] +
                       '\n' +
                       'ordine: '+
                       message['ordine'] +
                       '\n' +
                       'unitaMisura: '+
                       message['unitaMisura'] +
                       '\n' +
                       'newOrdineSottolav: {}'.format(
                       message['newOrdineSottolav'] ) +
                       '\n' +
                       'oldOrdineSottolav: {}'.format(
                       message['oldOrdineSottolav'] )+




                       ' \n\n\n')
    PreventivoEdile.iniziaRiordinoSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'], ordine=message['ordine'],
                                                   unitaMisura=message['unitaMisura'])

    PreventivoEdile.modificaOrdineSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                                   ordine=message['ordine'],
                                                   old_ordine_sottolavorazione=int('-' + message['oldOrdineSottolav']),
                                                   new_ordine_sottolavorazione=message['newOrdineSottolav'],
                                                   unitaMisura=message['unitaMisura'])


@socketio.on('modifica_sottolavorazione', namespace='/preventivoEdile')
def handle_modifica_sottolavorazione(message):

    app.server.logger.info("\n\nEntrato in mod_sottolav: messaggio: {}\n\n".format(message))

    message = json.loads(message)

    numero_preventivo = message.pop("numero_preventivo")
    data = message.pop("data")
    ordine = message.pop("ordine")
    ordine_sottolavorazione = message.pop("ordine_sottolavorazione")
    unitaMisura = message.pop("unitaMisura")

    PreventivoEdile.modificaSottolavorazione(numero_preventivo=numero_preventivo, data=data,
                                                 ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione,
                                                 modifica=message, unitaMisura=unitaMisura)


@socketio.on('stampa_preventivo', namespace='/preventivoEdile')
def handle_stampa_preventivo(message):
    app.server.logger.info('\n\nEntrato in stampa\n\n')
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoEdile.stampaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'])
    emit('procediADownload', namespace='/preventivoEdile', room=dip.session_id)


@socketio.on_error('/impegni')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))


@socketio.on_error('/home')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/notifica')
def error_handler_notifica(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/prezzario')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/fornitore')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/prezzarioProdotti')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/preventivoEdile')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))