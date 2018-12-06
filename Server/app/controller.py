from flask import render_template, redirect, request, url_for, session, request, send_from_directory
from app import server, socketio, accoglienzaForm
from .model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm, ClienteAccoltoForm, ApriPaginaClienteForm
from .model.dipendenteFittizio import DipendenteFittizio
from .model.dipendenteRegistrato import DipendenteRegistrato
from .model.dipendente import Dipendente
from .model.dirigente import Dirigente
from .model.notifica import Notifica
from .model.settoreLavorazione import SettoreLavorazione
from .model.prezzarioEdile import PrezzarioEdile
from .model.impiegoArtigiano import ImpiegoArtigiano
from .model.artigiano import Artigiano
from .model.clienteAccolto import ClienteAccolto
from .model.impegni import Impegni
from .model.fornitore import Fornitore
from .model.settoreMerceologico import SettoreMerceologico
from .model.personaleFornitore import PersonaleFornitore
from .model.tipologiaProdotto import TipologiaProdotto
from .model.modelloProdotto import ModelloProdotto
from .model.prodottoPrezzario import ProdottoPrezzario
from .model.capitolatoProdotto import CapitolatoProdotto
from .model.giorniPagamentoFornitore import GiorniPagamentoFornitore
from .model.modalitaPagamentoFornitore import ModalitaPagamentoFornitore
from .model.tipologiaPagamentoFornitore import TipologiaPagamentoFornitore
from .model.tempiDiConsegnaFornitore import TempiDiConsegnaFornitore
from .model.preventivoEdile import PreventivoEdile
from .model.preventivoFiniture import PreventivoFiniture
from .model.preventivoVarianti import PreventivoVarianti
from .model.eccezioni.righaPresenteException import RigaPresenteException
from .model.agenda import Agenda
from .model.calendario import Calendario
from .model.richiestaFerie import RichiestaFerie
from .model.messaggio import Messaggio
from flask_login import current_user, login_user, login_required, logout_user
from flask_socketio import emit, join_room, leave_room
import app
import json
import os


####################################### ROUTE HANDLER #################################################


@server.route('/prezzarioProdotti')
@login_required
def prezzarioProdotti():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    colleghi = Dipendente.query.all()
    fornitori = Fornitore.query.all()
    prodotti = ModelloProdotto.query.all()
    capitolati = CapitolatoProdotto.query.all()
    tipologia = TipologiaProdotto.query.all()

    return render_template('prezzarioProdotti.html', dipendente=dip, colleghi=colleghi, scheda=True,
                           prezzario_prodotti=True, fornitori=fornitori, prodotti=prodotti, capitolati=capitolati, tipologia=tipologia)

@server.route('/schedaFornitori', methods=['GET', 'POST'])
@login_required
def schedaFornitori():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    colleghi = Dipendente.query.all()
    fornitori = Fornitore.query.all()
    personale = PersonaleFornitore.query.all()
    settore_merceologico =SettoreMerceologico.query.all()

    tempiDiConsegna = TempiDiConsegnaFornitore.query.all()
    modalitaPagamento = ModalitaPagamentoFornitore.query.all()
    tipologiaPagamento = TipologiaPagamentoFornitore.query.all()
    giorniPagamento = GiorniPagamentoFornitore.query.all()


    return render_template('schedaFornitori.html', dipendente=dip, colleghi=colleghi, scheda=True,
                           scheda_fornitori=True, fornitori=fornitori, settore_merceologico=settore_merceologico,
                           personale=personale, tempiDiConsegna=tempiDiConsegna, modalitaPagamento=modalitaPagamento,
                           tipologiaPagamento=tipologiaPagamento, giorniPagamento=giorniPagamento)

@server.route('/PrezzarioEdile', methods=['GET', 'POST'])
@login_required
def prezzarioEdile():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    #colleghi = Dipendente.query.all()
    SettoreLavorazione.inizializza()
    settori = SettoreLavorazione.query.all()
    prezzario =PrezzarioEdile.query.first()
    lavorazioni =  PrezzarioEdile.returnLavorazioni()

    return render_template('prezzarioEdile.html', dipendente=dip, prezzario=prezzario, settori=settori, lavorazioni=lavorazioni,
                           scheda=True, prezzario_edile=True )


@server.route('/agendaClientePag/<dipUsername>')
@login_required
def agendaClientePag(dipUsername):
    dip = Dipendente.query.filter_by(username=dipUsername).first()

    agenda = Agenda.query.filter_by(dipendente=dipUsername)
    return render_template('paginaCliente_agenda.html', agenda=agenda, dipendente=dip)

@server.route('/gestioneDip', methods=['GET','POST'])
@login_required
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():

        DipendenteFittizio.registraDipendente(username=form.username.data, password=form.password.data,
                                                classe=form.tipo_dip.data, dirigente=form.dirigente.data, creatoreCredenziali=current_user.get_id())

        DipendenteFittizio.inviaCredenziali(email=form.email_dip.data, username=form.username.data, password=form.password.data)

        return redirect('/homepage')
    else:
        form.assegnaUserEPass()
        return render_template('gestioneDip.html', form=form )


@server.route('/uploadImgProfilo', methods=['POST'])
def upload_file():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    file = request.files['image']

    #Dipendente.salvaImmagineProfilo(dip.username, "{}.{}".format(dip.username, file.filename.split('.')[1] ))
    Dipendente.salvaImmagineProfilo(dip.username, file, dip )

    return redirect('/paginaProfilo')

@server.route('/paginaProfilo')
@login_required
def paginaProfilo():
    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    dipendenti = Dipendente.query.all()
    calendario = Calendario.query.filter_by(dipendente=dip.username).all()
    return render_template('paginaProfilo.html', dipendente=dip, dipendenti=dipendenti, calendario=calendario)


@server.route('/newPreventivoEdile')
@login_required
def newPreventivoEdile():

    settori = SettoreLavorazione.query.order_by( SettoreLavorazione.nome )
    prezzarioEdile = PrezzarioEdile.query.first()
    lavorazioni = PrezzarioEdile.returnLavorazioni()
    preventivo = PreventivoEdile.query.filter_by(numero_preventivo=app.preventivoEdileSelezionato[0], data=app.preventivoEdileSelezionato[1]).first()
    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()

    return render_template('preventivoEdile.html', codicePreventivo=codicePreventivo, settori=settori,
                            preventivoFullPage=True, cliente=cliente, prezzarioEdile=prezzarioEdile,
                            lavorazioni=lavorazioni, preventivo=preventivo, preventivoEdile=True)


@server.route('/apriPreventivoEdile')
@login_required
def apriPreventivoEdile():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    settori = SettoreLavorazione.query.order_by( SettoreLavorazione.nome )
    prezzarioEdile = PrezzarioEdile.query.first()
    lavorazioni = PrezzarioEdile.returnLavorazioni()
    preventivo = PreventivoEdile.query.filter_by(numero_preventivo=app.preventivoEdileSelezionato[0], data=app.preventivoEdileSelezionato[1]).first()
    infoPreventivo = PreventivoEdile.returnSinglePreventivo(numero_preventivo=app.preventivoEdileSelezionato[0], data=app.preventivoEdileSelezionato[1])
    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()

    return render_template('preventivoEdile.html', codicePreventivo=codicePreventivo, settori=settori,
                            preventivoFullPage=True, cliente=cliente, prezzarioEdile=prezzarioEdile, lavorazioni=lavorazioni,
                            preventivo=preventivo, preventivoEdile=True, infoPreventivo=infoPreventivo, dipendente=dip)

@server.route('/downloadPreventivoEdile')
@login_required
def downloadPreventivoEdile():
    return send_from_directory(directory='preventiviLatexDir', filename='preventivoEdile.pdf')

@server.route('/downloadPreventivoVarianti')
@login_required
def downloadPreventivoVarianti():
    return send_from_directory(directory='preventiviLatexDir', filename='preventivoVarianti.pdf')

@server.route('/downloadPreventivoFiniture')
@login_required
def downloadPreventivoFiniture():
    return send_from_directory(directory='preventiviLatexDir', filename='preventivoFiniture.pdf')

@server.route('/apriPreventivoFiniture')
@login_required
def apriPreventivoFiniture():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    tipologie = TipologiaProdotto.query.all()
    prezzarioProdotti = ProdottoPrezzario.query.all()
    modelliProdotto = ModelloProdotto.query.all()
    capitolatiProdotto = CapitolatoProdotto.query.all()




    preventivo = PreventivoFiniture.query.filter_by(numero_preventivo=app.preventivoFinitureSelezionato[0], data=app.preventivoFinitureSelezionato[1]).first()
    prodottiPreventivo = PreventivoFiniture.returnProdottiPreventivo(numero_preventivo=app.preventivoFinitureSelezionato[0], data=app.preventivoFinitureSelezionato[1])

    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()

    return render_template('preventivoFiniture.html', codicePreventivo=codicePreventivo, tipologie=tipologie,
                            modelliProdotto=modelliProdotto,
                            preventivoFullPage=True, cliente=cliente, prezzarioProdotti=prezzarioProdotti,
                            preventivo=preventivo, preventivoFiniture=True, prodottiPreventivo=prodottiPreventivo,
                            dipendente=dip, capitolatiProdotto=capitolatiProdotto )

@server.route('/apriPreventivoVarianti')
@login_required
def apriPreventivoVarianti():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    settori = SettoreLavorazione.query.all()
    prezzarioEdile = PrezzarioEdile.query.all()
    preventivo = PreventivoVarianti.query.filter_by(numero_preventivo=app.preventivoVariantiSelezionato[0], data=app.preventivoVariantiSelezionato[1]).first()
    infoPreventivo = PreventivoVarianti.returnSinglePreventivo(numero_preventivo=app.preventivoVariantiSelezionato[0], data=app.preventivoVariantiSelezionato[1])
    cliente = ClienteAccolto.query.filter_by(nome=preventivo.nome_cliente, cognome=preventivo.cognome_cliente, indirizzo=preventivo.indirizzo_cliente).first()
    codicePreventivo=preventivo.calcolaCodicePreventivo()
    capitolatiProdotto = CapitolatoProdotto.query.all()

    return render_template('preventivoVarianti.html', codicePreventivo=codicePreventivo, settori=settori,
                            preventivoFullPage=True, cliente=cliente, prezzarioEdile=prezzarioEdile,
                            preventivo=preventivo, preventivoFiniture=True, infoPreventivo=infoPreventivo,
                            dipendente=dip, capitolatiProdotto=capitolatiProdotto )

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

    colleghi = Dipendente.query.all()

    return render_template('paginaCliente.html', colleghi=colleghi,
                           dipendente=dip, cliente=app.clienteSelezionato, ufficioCommerciale=ufficioCommerciale,
                           ufficioTecnico=ufficioTecnico, ufficioCapicantiere=ufficioCapicantiere )

@server.route('/clientBack')
@login_required
def clientBack():

    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    ufficioCommerciale = []#Dipendente.query.filter_by( classe="commerciale", username=cliente.commerciale )
    ufficioTecnico = []#Dipendente.query.filter_by( classe="tecnico", username=cliente.tecnico )
    ufficioCapicantiere = []#Dipendente.query.filter_by( classe="commerciale", username=cliente.capocantiere )

    colleghi = Dipendente.query.all()

    return render_template('paginaCliente.html', dipendente=dip, colleghi=colleghi, cliente=app.clienteSelezionato, ufficioCommerciale=ufficioCommerciale,
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
            preventivi_distinti.append((preventivo[0].intervento_commessa, preventivo[0].calcolaCodicePreventivo(),
                                        preventivo[0].numero_preventivo))

    lastPrev = PreventivoEdile.returnLastPreventivoCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    countPreventivi = PreventivoEdile.get_counter_preventivi_per_cliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    return render_template('paginaCliente_prevEdile.html', dipendente=dip, cliente=app.clienteSelezionato,
                           preventivi=preventivi, preventivi_distinti=preventivi_distinti,
                           lastPreventivo=lastPrev, countPreventivi=countPreventivi)

@server.route('/anteprimaPreventivoFiniture')
@login_required
def anteprimaPreventivoFiniture():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    preventivi = PreventivoFiniture.returnAllPreventiviCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    preventivi_distinti = []

    for preventivo in preventivi:
        preventivo_presente = False
        for prev_dist in preventivi_distinti:
            if preventivo[0].numero_preventivo == prev_dist[2]:
                preventivo_presente = True

        if not preventivo_presente:
            preventivi_distinti.append((preventivo[0].intervento_commessa, preventivo[0].calcolaCodicePreventivo(),
                                        preventivo[0].numero_preventivo))

    countPreventivi = PreventivoFiniture.get_counter_preventivi_per_cliente(nome_cliente=app.clienteSelezionato.nome,
                                                                         cognome_cliente=app.clienteSelezionato.cognome,
                                                                         indirizzo_cliente=app.clienteSelezionato.indirizzo)

    lastPrev = PreventivoFiniture.returnLastPreventivoCliente(nome_cliente=app.clienteSelezionato.nome,
                                                           cognome_cliente=app.clienteSelezionato.cognome,
                                                           indirizzo_cliente=app.clienteSelezionato.indirizzo)

    preventiviEdili = PreventivoEdile.returnAllPreventiviCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    preventiviEdili_distinti = []

    for preventivo in preventiviEdili:
        preventivo_presente = False
        for prev_dist in preventiviEdili_distinti:
            if preventivo[0].numero_preventivo == prev_dist[2]:
                preventivo_presente = True

        if not preventivo_presente:
            preventiviEdili_distinti.append((preventivo[0].intervento_commessa, preventivo[0].calcolaCodicePreventivo(),
                                        preventivo[0].numero_preventivo))

    return render_template('paginaCliente_prevFiniture.html', dipendente=dip, cliente=app.clienteSelezionato, countPreventiviFiniture=countPreventivi,
                           preventiviFiniture_distinti=preventivi_distinti, preventiviFiniture=preventivi,
                           lastPreventivoFiniture=lastPrev, preventiviEdili_distinti=preventiviEdili_distinti)

@server.route('/anteprimaPreventivoVarianti')
@login_required
def anteprimaPreventivoVarianti():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()


    preventiviEdili = PreventivoEdile.returnAllPreventiviCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    preventiviEdili_distinti = []

    for preventivo in preventiviEdili:
        preventivo_presente = False
        for prev_dist in preventiviEdili_distinti:
            if preventivo[0].numero_preventivo == prev_dist[2]:
                preventivo_presente = True

        if not preventivo_presente:
            preventiviEdili_distinti.append((preventivo[0].intervento_commessa, preventivo[0].calcolaCodicePreventivo(),
                                        preventivo[0].numero_preventivo))


    preventiviVarianti = PreventivoVarianti.returnAllPreventiviCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    preventiviVarianti_distinti = []

    for preventivo in preventiviVarianti:
        preventivo_presente = False
        for prev_dist in preventiviVarianti_distinti:
            if preventivo[0].numero_preventivo == prev_dist[2]:
                preventivo_presente = True

        if not preventivo_presente:
            preventiviVarianti_distinti.append((preventivo[0].intervento_commessa, preventivo[0].calcolaCodicePreventivo(),
                                        preventivo[0].numero_preventivo))

    lastPrev = PreventivoVarianti.returnLastPreventivoCliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    countPreventiviVarianti = PreventivoVarianti.get_counter_preventivi_per_cliente(nome_cliente=app.clienteSelezionato.nome, cognome_cliente=app.clienteSelezionato.cognome,
                                                        indirizzo_cliente=app.clienteSelezionato.indirizzo )

    return render_template('paginaCliente_prevVarianti.html', dipendente=dip, cliente=app.clienteSelezionato,
                           preventiviVarianti=preventiviVarianti, preventiviVarianti_distinti=preventiviVarianti_distinti,
                           preventiviEdili_distinti=preventiviEdili_distinti,
                           lastPreventivoVarianti=lastPrev, countPreventiviVarianti=countPreventiviVarianti)

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
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    if error == 1 or error == 2 :

        if app.accoglienzaOk:
            app.accoglienzaOk=False

            if error == 1:
                return render_template('confermaRegistrazioneCliente.html', dipendente=dip)
            else:
                app.server.logger.info('\n\n\npreventivo apriti\n\n')
                return redirect('/newPreventivoEdile')
        else:
            return render_template('accoglienzaCliente.html', form=app.accoglienzaForm)

    app.accoglienzaForm = ClienteAccoltoForm(request.form)

    if request.method == 'POST':

        app.server.logger.info('\n\n\nprevalidate\n\n')
        if app.accoglienzaForm.validate_on_submit():
            app.server.logger.info('\n\n\nvalidato\n\n')
            ClienteAccolto.registraCliente(nome=app.accoglienzaForm.nome.data, cognome=app.accoglienzaForm.cognome.data, indirizzo=app.app.accoglienzaForm.indirizzo.data,
                                           telefono=app.accoglienzaForm.telefono.data, email=app.accoglienzaForm.email.data, difficolta=app.accoglienzaForm.difficolta.data,
                                           tipologia=app.accoglienzaForm.tipologia.data, referenza=app.accoglienzaForm.referenza.data, sopraluogo=app.accoglienzaForm.sopraluogo.data,
                                           lavorazione=app.accoglienzaForm.lavorazione.data, commerciale=current_user.get_id())

            app.accoglienzaOk=True
            return render_template('confermaRegistrazioneCliente.html', dipendente=dip)

    server.logger.info("\n\nAlternativa al post {}{}\n\n".format(app.accoglienzaForm.nome.errors, app.accoglienzaForm))

    return render_template('accoglienzaCliente.html', form=app.accoglienzaForm)



@server.route('/homepage')
@login_required
def homepage():

    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    colleghi = Dipendente.query.all()
    agenda=Agenda.query.filter_by(dipendente=dip.username).all()
    calendario=Calendario.query.all()
    impegni = Impegni.query.filter_by(dipendente=current_user.get_id())

    return render_template('homepage.html', impegni=impegni, dipendente=dip, colleghi=colleghi, agenda=agenda, calendario=calendario, sockUrl=app.appUrl)

@server.route('/chat')
@login_required
def chat():

    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    colleghi = Dipendente.query.all()

    return render_template('chat.html', colleghi=colleghi, dipendente=dip, sockUrl=app.appUrl)


@server.route('/sidebarLeft')
@login_required
def sidebarLeft():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('sidebar-left.html', dipendente=dip)

@server.route('/schedaArtigiani')
@login_required
def schedaArtigiani():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    colleghi = Dipendente.query.all()
    artigiani = Artigiano.query.all()
    impieghi = ImpiegoArtigiano.query.all()

    return render_template('schedaArtigiani.html', dipendente=dip, colleghi=colleghi, artigiani=artigiani,
                                impieghi=impieghi, scheda=True, scheda_artigiani=True)

@server.route('/header')
@login_required
def header():

    app.formCercaCliente = ApriPaginaClienteForm(request.form)

    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()

    listaClienti = []


    listaClienti = ClienteAccolto.query.order_by(ClienteAccolto.cognome, ClienteAccolto.nome).all()



    numNot = Notifica.get_counter(destinatario=current_user.get_id())
    return render_template('header.html', dipendente=dip, numNotifiche=numNot, listaClienti=listaClienti, form=app.formCercaCliente)

@server.route('/registraDipendente', methods=['GET','POST'])
@login_required
def registraDipendente():
    form = RegistraDipendenteForm()

    if form.validate_on_submit():

        if Dipendente.query.filter_by(cf=form.cf.data).first() != None:
            return render_template("registrazioneDip.html", form=form, fittizio=True, errCf=True)

        domicilioDip = form.resEDomUguali.data
        domicilioVia = ''
        domicilioNum = ''
        domicilioCitta = ''
        domicilioCap = ''
        domicilioRegione = ''



        if domicilioDip:
            domicilioVia = form.residenzaVia.data
            domicilioNum = form.residenzaNum.data
            domicilioCitta = form.residenzaCitta.data
            domicilioCap = form.residenzaCap.data
            domicilioRegione = form.residenzaRegione.data
        else:

            domicilioVia = form.domicilioVia.data
            domicilioNum = form.domicilioNum.data
            domicilioCitta = form.domicilioCitta.data
            domicilioCap = form.domicilioCap.data
            domicilioRegione = form.domicilioRegione.data

        ( username, password, creatoreCredenziali ) = Dipendente.registraDipendente(dipFitUsername=current_user.get_id(), nome=form.nome.data, cognome=form.cognome.data,
                                cf=form.cf.data, dataNascita=form.dataNascita.data,
                                residenzaVia=form.residenzaVia.data, residenzaNum=form.residenzaNum.data, residenzaCitta=form.residenzaCitta.data,
                                residenzaCap=form.residenzaCap.data, residenzaRegione=form.residenzaRegione.data,
                                domicilioVia=domicilioVia, domicilioNum=domicilioNum, domicilioCitta=domicilioCitta,
                                domicilioCap=domicilioCap,
                                domicilioRegione=domicilioRegione, telefono=form.telefono.data,
                                password=form.password.data,
                                email_personale=form.email_personale.data, iban=form.iban.data, partitaIva=form.partitaIva.data )


        return render_template("confermaRegistrazione.html", username=username, password=password, creatoreCredenziali=creatoreCredenziali, sockUrl=app.appUrl )

    return render_template("registrazioneDip.html", form=form, fittizio=True)

@server.route('/tmp')
def tmp():
    return render_template("confermaRegistrazione.html", username='paolo', password='tizio',
                            sockUrl=app.appUrl)


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


    notiche = Notifica.getNotificheOrdinate(destinatario=current_user.get_id())

    returnList = ""

    for nota in notiche:


        returnList += '{ "titolo": "' +nota.titolo+ '", "contenuto": "' + nota.contenuto +'", "tipologia": "'+nota.tipologia+'", "numero_nota": "'+str(nota.numero)+'"  },'



    return '{ "list":[' +returnList[:-1]+'] }'


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

@socketio.on('richiedi_notifiche_dipendente', namespace="/notifica")
def handle_richiedi_notifiche_dipendente(message):
    #usato inizialmente per recuperare le notifiche da mostrare
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    notifiche = Notifica.getNotificheOrdinate(message['dip'])

    for notifica in notifiche:
        emit('aggiornaNotifiche', {'titolo': notifica.titolo,
                                   'contenuto': notifica.contenuto,
                                   'tipologia': notifica.tipologia,
                                   'numero': notifica.numero}, namespace='/notifica', room=dip.session_id)

@socketio.on('registrazione_effettuata', namespace="/notifica")
def handle_registrazione_effetuata(message):
    responsabile = Dipendente.query.filter_by(username=message['responsabile']).first()
    nuovoDip = Dipendente.query.filter_by(username=message['dipendente_registrato']).first()


    num= Notifica.registraNotifica(destinatario=responsabile.username, titolo="Aggiunto dipendente {0} {1}".format(nuovoDip.nome, nuovoDip.cognome),
                              contenuto="Ricorda di completare la sua registrazione.")

    emit('aggiornaNotifiche', {'titolo': "Aggiunto dipendente {0} {1}".format(nuovoDip.nome, nuovoDip.cognome),
                               'contenuto': "Ricorda di completare la sua registrazione.", 'tipologia' : "newDip",
                               'numero': num},
                                namespace='/notifica', room=responsabile.session_id)



@socketio.on('elimina_nota', namespace="/notifica")
def handle_elimina_nota(message):

    Notifica.eliminaNotifica(destinatario=message['dipendente'], numero=message['numero_notifica'])

@socketio.on('accetta_ferie', namespace="/notifica")
def handle_accetta_ferie(message):

    dirigente = Dipendente.query.filter_by(username=message['dirigente']).first()

    notifica = Notifica.query.filter_by(destinatario=dirigente.username, numero=message['numero_notifica']).first()

    richiedente_ferie = Dipendente.query.filter_by(username=notifica.richiedente_ferie).first()

    notificheFerieInviate = Notifica.query.filter_by(richiedente_ferie=richiedente_ferie.username,
                                                     start_date=notifica.start_date).all()

    #Elimino ad ogni dirigente la notifica della richiesta ferie realtime

    for nota in notificheFerieInviate:
        responsabile = Dipendente.query.filter_by(username=nota.destinatario).first()
        emit('eliminaNotifica', {'numero': nota.numero}, namespace='/notifica', room=responsabile.session_id)

    RichiestaFerie.accettaRichiesta(dipendente=notifica.richiedente_ferie, start_date=notifica.start_date)

    # invio la nota dell'accettazione al dipendente interessato
    num=Notifica.registraNotifica(destinatario=richiedente_ferie.username,
                              titolo="Richiesta ferie accettata da {} {}".format(dirigente.nome, dirigente.cognome),
                              contenuto="Commento del dirigente: {}".format(message['nota_dirigente']), tipologia="commonNote" )

    emit('aggiornaNotifiche', {'titolo': "Richiesta ferie accettata da {} {}".format(dirigente.nome, dirigente.cognome),
                               'contenuto': "Commento del dirigente: {}".format(message['nota_dirigente']),
                               'tipologia': "commonNote", 'numero': num},
         namespace='/notifica', room=richiedente_ferie.session_id)



    Notifica.eliminaNotificaFerie(richiedente_ferie=richiedente_ferie.username, start_date=notifica.start_date)


@socketio.on('declina_ferie', namespace="/notifica")
def handle_declina_ferie(message):
    dirigente = Dipendente.query.filter_by(username=message['dirigente']).first()

    notifica = Notifica.query.filter_by(destinatario=dirigente.username, numero=message['numero_notifica']).first()

    richiedente_ferie = Dipendente.query.filter_by(username=notifica.richiedente_ferie).first()

    notificheFerieInviate = Notifica.query.filter_by(richiedente_ferie=richiedente_ferie.username,
                                                     start_date=notifica.start_date).all()

    # Elimino ad ogni dirigente la notifica della richiesta ferie realtime

    for nota in notificheFerieInviate:
        responsabile = Dipendente.query.filter_by(username=nota.destinatario).first()
        emit('eliminaNotifica', {'numero': nota.numero}, namespace='/notifica', room=responsabile.session_id)

    RichiestaFerie.declinaRichiesta(dipendente=notifica.richiedente_ferie, start_date=notifica.start_date)


    # invio la nota dell'accettazione al dipendente interessato
    num=Notifica.registraNotifica(destinatario=richiedente_ferie.username,
                              titolo="Richiesta ferie rifiutata da {} {}".format(dirigente.nome, dirigente.cognome),
                              contenuto="Commento del dirigente: {}".format(message['nota_dirigente']), tipologia="commonNote")

    emit('aggiornaNotifiche', {'titolo': "Richiesta ferie rifiutata da {} {}".format(dirigente.nome, dirigente.cognome),
                               'contenuto': "Commento del dirigente: {}".format(message['nota_dirigente']),
                               'tipologia': "commonNote", 'numero': num},
         namespace='/notifica', room=richiedente_ferie.session_id)

    # elimino la nota del dirigente
    Notifica.eliminaNotificaFerie(richiedente_ferie=richiedente_ferie.username, start_date=notifica.start_date)

@socketio.on('registra_settore_lavorazione', namespace="/prezzario")
def handle_registra_settore(message):
    SettoreLavorazione.registraSettore(nome=message['settore'])

@socketio.on('elimina_settore_lavorazione', namespace="/prezzario")
def handle_elimina_settore(message):
    SettoreLavorazione.eliminaSettore(nome=message['nome'])

@socketio.on('modifica_settore_lavorazione', namespace="/prezzario")
def handle_elimina_settore(message):
    SettoreLavorazione.modificaSettore(oldNome=message['oldNome'], newNome=message['newNome'])

@socketio.on('registra_lavorazione', namespace="/prezzario")
def handle_registra_lavorazione(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()


    SettoreLavorazione.registraSettore(nome=message['settore'])


    PrezzarioEdile.registraLavorazione(settore=message["settore"], tipologia_lavorazione=message["tipologia"],
                                        pertinenza=message["pertinenza"], unitaMisura=message["unita"],
                                         prezzoMin=message["pMin"], prezzoMax=message["pMax"],
                                          dimensione=message["dimensione"], fornitura=message["fornitura"], posa=message["posa"],
                                            note=message["note"])
    emit('confermaRegistrazioneLavorazione', namespace='/prezzario', room=dip.session_id)

@socketio.on('modifica_lavorazione', namespace="/prezzario")
def handle_modifica_lavorazione(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PrezzarioEdile.modificaLavorazione(settore=message["settore"], tipologia_lavorazione=message["tipologia"],
                                        modifica={message['toEdit'] : message['valore']})

    emit('conferma_modifica_lavorazione', namespace='/prezzario', room=dip.session_id)


@socketio.on('modifica_ricarico_prezzario', namespace='/prezzario')
def handle_modifica_ricarico_all(message):

    PrezzarioEdile.modificaRicaricoPrezzario(message['valore']);

@socketio.on('settaLavorazioneDaVerificare', namespace='/prezzario')
def handle_setta_daVerificare(message):
    PrezzarioEdile.setDaVerificare(settore=message['settore'], tipologia_lavorazione=message['tipologia'], valore=message['valore'])

@socketio.on('elimina_lavorazione', namespace='/prezzario')
def handle_elimina_lavorazione(message):
    PrezzarioEdile.eliminaLavorazione(settore=message['settore'], tipologia_lavorazione=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('conferma_elimina_lav', namespace='/prezzario', room=dip.session_id)


@socketio.on('notifica_del_nota_imposta', namespace="/impegni")
def handle_notifica_del_nota_imposta(message):
    dir = Dipendente.query.filter_by(username=message['dir']).first()

    num=Notifica.registraNotifica(destinatario=dir.username,
                              titolo="Impegno svolto",
                              contenuto= "{} ha svolto l'impegno:<br/> {}".format(message['dip'], message['impegno']),
                              tipologia='commonNote')

    emit('aggiornaNotifiche', {'titolo': "Impegno svolto",
                               'contenuto': "{} ha svolto l'impegno:<br/> {}".format(message['dip'], message['impegno']),
                               'tipologia': "commonNote", 'numero': num},  namespace='/notifica', room=dir.session_id)


@socketio.on('registraImpegno', namespace='/impegni')
def handle_registraImpegno(message):

    numeroETipologia = None

    if message['dir'] == "":
        numeroETipologia = Impegni.registraImpegni(dipendente=message['dip'], testo=message['testo'])
    else:
        numeroETipologia = Impegni.registraImpegni(dipendente=message['dip'], testo=message['testo'], dirigente=message['dir'])

        dir = Dipendente.query.filter_by(username=message['dir']).first()

        emit('conferma_impegno_inviato', namespace='/impegni', room=dir.session_id )

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    emit('aggiungiImpegno', {'testo': message['testo'], 'numero': numeroETipologia[0], 'tipologia': numeroETipologia[1]}, namespace='/impegni', room=dip.session_id)



@socketio.on('checkaImpegno', namespace='/impegni')
def handle_checkaImpegno(message):

    Impegni.check(dipendente=message['dipendente'], id=message['numero'])

@socketio.on('eliminaImpegno', namespace='/impegni')
def handle_eliminaImpegno(message):
    Impegni.eliminaImpegni(dipendente=message['dipendente'], id=message['numero'])

@socketio.on('registra_personale', namespace='/fornitore')
def handle_registra_personale(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()


    returnStatus = PersonaleFornitore.registraRappresentante(nome=message['nome'], cognome=message['cognome'],
                                                             ruolo=message['ruolo'], telefono=message['telefono'],
                                                             email=message['email'],
                                                             azienda_primo_gruppo=message['primo_gruppo'],
                                                             azienda_sotto_gruppo=message['sotto_gruppo'])

    emit('rispostaRegistraPersonale', {'status': returnStatus[0], 'risposta': returnStatus[1]}, namespace='/fornitore',
         room=dip.session_id)

@socketio.on('elimina_personale_fornitore', namespace='/fornitore')
def handle_elimina_personale_fornitore(message):

    PersonaleFornitore.eliminaRappresentante(nome=message['nome'], cognome=message['cognome'],
                                             azienda_primo_gruppo=message['primo_gruppo'], azienda_sotto_gruppo=message['sotto_gruppo'])


@socketio.on('registraFornitore', namespace='/fornitore')
def handle_registraFornitore(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    SettoreMerceologico.registraSettore(nome=message['settoreMerceologico'])
    TempiDiConsegnaFornitore.registraTempiDiConsegna(nome=message['tempiDiConsegna'])
    TipologiaPagamentoFornitore.registraTipologiaPagamento(nome=message['tipologiaPagamenti'])
    ModalitaPagamentoFornitore.registraModalitaPagamento(nome=message['modalitaPagamenti'])
    GiorniPagamentoFornitore.registraGiorniPagamento(nome=message['giorniPagamenti'])

    returnStatus = Fornitore.registraFornitore(primo_gruppo=message['primo_gruppo'],   sotto_gruppo=message['sotto_gruppo'],
                            settoreMerceologico = message['settoreMerceologico'], stato=message['stato'],
                            tempiDiConsegna = message['tempiDiConsegna'], prezziNetti = message['prezziNetti'],
                            scontoStandard = message['scontoStandard'], scontoExtra1 = message['scontoExtra1'],
                            scontoExtra2 = message['scontoExtra2'], trasporto=message['trasporto'],
                            imballo=message['imballo'], montaggio=message['montaggio'],
                            trasportoUnitaMisura=message['trasportoUnitaMisura'],
                            imballoUnitaMisura=message['imballoUnitaMisura'], montaggioUnitaMisura=message['montaggioUnitaMisura'],
                            giorniPagamenti = message['giorniPagamenti'], modalitaPagamenti = message['modalitaPagamenti'],
                            tipologiaPagamenti = message['tipologiaPagamenti'], provincia = message['provincia'],
                            indirizzo = message['indirizzo'], telefono = message['telefono'], sito = message['sito'])

    emit('rispostaRegistraFornitore', {'status':returnStatus[0], 'risposta':returnStatus[1]}, namespace='/fornitore', room=dip.session_id )

@socketio.on('modificaFornitore', namespace='/fornitore')
def handle_modificaFornitore(message):

    app.server.logger.info('chiamato {}\n\n\n'.format(message['toEdit']))
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    if message['toEdit'] == 'tempiDiConsegna':
        TempiDiConsegnaFornitore.registraTempiDiConsegna(nome=message['value'])
    elif message['toEdit'] == 'tipologiaPagamenti':
        TipologiaPagamentoFornitore.registraTipologiaPagamento(nome=message['value'])
    elif message['toEdit'] == 'modalitaPagamenti':
        ModalitaPagamentoFornitore.registraModalitaPagamento(nome=message['value'])
    elif message['toEdit'] == 'giorniPagamenti':
        GiorniPagamentoFornitore.registraGiorniPagamento(nome=message['value'])



    Fornitore.modificaFornitore(primo_gruppo=message['primo_gruppo'], sotto_gruppo=message['sotto_gruppo'],
                                modifica={message['toEdit']: message['value']})


    emit('confermaModifica', {'primo_gruppo': message['primo_gruppo'], 'sotto_gruppo': message['sotto_gruppo'],
                               'toEdit': message['toEdit'], 'value': message['value'] },
             namespace='/fornitore', room=dip.session_id )



@socketio.on('eliminaFornitore', namespace='/fornitore')
def handle_eliminaFornitore(message):

    Fornitore.eliminaFornitore(primo_gruppo=message['primo_gruppo'], sotto_gruppo=message['sotto_gruppo'])

@socketio.on('modifica_giorno_pagamento', namespace="/fornitore")
def handle_registra_giorno_pagamento(message):
    GiorniPagamentoFornitore.modificaGiorniPagamento(newNome=message['newNome'], oldNome=message['oldNome'])


@socketio.on('elimina_giorno_pagamento', namespace="/fornitore")
def handle_elimina_giorno_pagamento(message):
    GiorniPagamentoFornitore.eliminaGiorniPagamento(nome=message['nome'])

@socketio.on('modifica_modalita_pagamento', namespace="/fornitore")
def handle_modifica_modalita_pagamento(message):
    ModalitaPagamentoFornitore.modificaModalitaPagamento(newNome=message['newNome'], oldNome=message['oldNome'])


@socketio.on('elimina_modalita_pagamento', namespace="/fornitore")
def handle_elimina_modalita_pagamento(message):
    ModalitaPagamentoFornitore.eliminaModalitaPagamento(nome=message['nome'])


@socketio.on('modifica_tipologia_pagamento', namespace="/fornitore")
def handle_modifica_tipologia_pagamento(message):
    TipologiaPagamentoFornitore.modificaTipologiaPagamento(newNome=message['newNome'], oldNome=message['oldNome'])


@socketio.on('elimina_tipologia_pagamento', namespace="/fornitore")
def handle_elimina_tipologia_pagamento(message):
    TipologiaPagamentoFornitore.eliminaTipologiaPagamento(nome=message['nome'])

@socketio.on('modifica_tempi_di_consegna', namespace="/fornitore")
def handle_modifica_tempi_di_consegna(message):
    TempiDiConsegnaFornitore.modificaTempiDiConsegna(newNome=message['newNome'], oldNome=message['oldNome'])


@socketio.on('elimina_tempi_di_consegna', namespace="/fornitore")
def handle_elimina_tempi_di_consegna(message):
    TempiDiConsegnaFornitore.eliminaTempiDiConsegna(nome=message['nome'])

@socketio.on('modifica_settore_merceologico', namespace="/fornitore")
def handle_modifica_settore_merceologico(message):
    SettoreMerceologico.modificaSettore(newNome=message['newNome'], oldNome=message['oldNome'])


@socketio.on('elimina_settore_merceologico', namespace="/fornitore")
def handle_elimina_settore_merceologico(message):
    SettoreMerceologico.eliminaSettore(nome=message['nome'])

@socketio.on('registra_artigiano', namespace="/artigiani")
def handle_registra_artigiano(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    ImpiegoArtigiano.registraImpiego(nome=message['impiego'])

    Artigiano.registraArtigiano( nominativo=message['nominativo'], impiego=message['impiego'],
                                 valutazione=message['valutazione'], contatti1=message['contatti1'],
                                 contatti2=message['contatti2'], email=message['email'],
                                 note=message['note'])

    emit('confermaRegistrazioneArtigiano', namespace='/artigiani', room=dip.session_id)

@socketio.on('modifica_artigiano', namespace="/artigiani")
def handle_modifica_artigiano(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    Artigiano.modificaArtigiano(nominativo=message['nominativo'], impiego=message['impiego'],
                                modifica={message['toEdit'] : message['valore']})

    emit('conferma_modifica_artigiano', namespace='/artigiani', room=dip.session_id)

@socketio.on('modifica_colore_artigiano', namespace="/artigiani")
def handle_modifica_artigiano(message):

    Artigiano.modificaColore(nominativo=message['nominativo'], impiego=message['impiego'], colore=message['colore'])

@socketio.on('elimina_artigiano', namespace='/artigiani')
def handle_elimina_artigiano(message):

    Artigiano.eliminaArtigiano(nominativo=message['nominativo'], impiego=message['impiego'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    emit('conferma_elimina_artigiano', namespace='/artigiani', room=dip.session_id)

@socketio.on('modifica_impiego', namespace="/artigiani")
def handle_modifica_impiego(message):

    ImpiegoArtigiano.modificaImpiego(oldNome=message['oldNome'], newNome=message['newNome'])

@socketio.on('elimina_impiego', namespace='/artigiani')
def handle_elimina_impiego(message):

    ImpiegoArtigiano.eliminaImpiego(nome=message['nome'])

@socketio.on('registra_prodotto', namespace='/prezzarioProdotti')
def handle_registra_prodotto(message):


    dip = Dipendente.query.filter_by(username=message['dip']).first()

    TipologiaProdotto.registraTipologiaProdotto(nome=message['tipologia'])


    ProdottoPrezzario.registraProdotto(nome=message['nome'], tipologia=message['tipologia'])

    ModelloProdotto.registraModello(nome=message['modello'],
                                    prodotto=message['nome'], tipologia=message['tipologia'],
                                    marchio=message['marchio'],
                                    codice=message['codice'],

                                    fornitore_primo_gruppo=message['fornitore_primo_gruppo'],
                                    fornitore_sotto_gruppo=message['fornitore_sotto_gruppo'],

                                    prezzoListinoFornitura=message['prezzoListinoFornitura'],
                                    nettoUsFornitura=message['nettoUsFornitura'],
                                    posa=message['posa'],
                                    posaPerc=message['posaPerc'],
                                    rincaroCliente=message['rincaroCliente'],
                                    versoDiLettura=message['versoDiLettura'],
                                    rincaroAzienda=message['rincaroAzienda'],
                                    trasportoAzienda=message['trasportoAzienda'],
                                    imballoAzienda=message['imballoAzienda'],
                                    trasportoAziendaUnitaMisura=message['trasportoAziendaUnita'],
                                    imballoAziendaUnitaMisura=message['imballoAziendaUnita']

                                    )

    if message['capitolato']:
        CapitolatoProdotto.registraCapitolato(nome=message['nome'], modello=message['modello'],
                                              tipologia=message['tipologia'], marchio=message['marchio'])

    emit( 'confermaRegistrazioneProdotto',  namespace='/prezzarioProdotti', room=dip.session_id)


@socketio.on('elimina_prodotto', namespace='/prezzarioProdotti')
def handle_elimina_prodotto(message):
    ProdottoPrezzario.eliminaProdotto(nome=message['prodotto'], tipologia=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()

@socketio.on('modifica_prodotto_dati', namespace='/prezzarioProdotti')
def handle_modifica_prodotto_dati(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    if message['toEdit'] == "nome_modello":
        message['toEdit']="nome"
    elif message['toEdit'] == 'nome_prodotto':
        ProdottoPrezzario.modificaProdotto(nome=message['prodotto'], tipologia=message['tipologia'], modifica={'nome': message['value']})
        message['toEdit'] = "prodotto"
    elif message['toEdit'] == 'tipologia':
        TipologiaProdotto.modificaTipologiaProdotto(nome=message['value'], oldNome=message['tipologia'] )


    if message['toEdit'] == 'fornitore':
        if  message['value'].endswith('-'):
            ModelloProdotto.modificaModello(nome=message['modello'], prodotto=message['prodotto'],
                                            tipologia=message['tipologia'], marchio=message['marchio'],
                                            modifica={'fornitore_primo_gruppo': message['value'].split(' -')[0] })
        elif message['value'].startswith('-'):
            ModelloProdotto.modificaModello(nome=message['modello'], prodotto=message['prodotto'],
                                            tipologia=message['tipologia'], marchio=message['marchio'],
                                            modifica={
                                                      'fornitore_sotto_gruppo': message['value'].split('- ')[1] })
        else:

            ModelloProdotto.modificaModello(nome=message['modello'], prodotto=message['prodotto'],
                                            tipologia=message['tipologia'], marchio=message['marchio'],
                                            modifica={ 'fornitore_primo_gruppo': message['value'].split(' - ')[0],
                                                       'fornitore_sotto_gruppo': message['value'].split(' - ')[1],
                                                   })
    else:
        ModelloProdotto.modificaModello(nome=message['modello'], prodotto=message['prodotto'],
                                        tipologia=message['tipologia'], marchio=message['marchio'],
                                        modifica={message['toEdit'] : message['value']})



    emit('confermaModificaProdotto', { 'modello': message['modello'], 'prodotto': message['prodotto'],
                               'tipologia':message['tipologia'],
                               'marchio': message['marchio'], 'toEdit': message['toEdit'], 'value': message['value']},namespace='/prezzarioProdotti', room=dip.session_id)



@socketio.on('modifica_prodotto_calcoli', namespace='/prezzarioProdotti')
def handle_modifica_prodotto_calcoli(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    ModelloProdotto.modificaModello(nome=message['modello'], prodotto=message['prodotto'],
                                    tipologia=message['tipologia'], marchio=message['marchio'],
                                    modifica={
                                        'prezzoListinoFornitura': message['listinoProdotto'],
                                        'nettoUsFornitura': message['usProdotto'],
                                        'posa': message['posa'],
                                        'posaPerc': message['posaPerc'],
                                        'rincaroCliente': message['rincaroCliente'],
                                        'rincaroAzienda': message['rincaroAzienda'],
                                        'trasportoAzienda': message['trasportoAzienda'],
                                        'trasportoAziendaUnitaMisura': message['trasportoAziendaUnita'],
                                        'imballoAzienda': message['imballoAzienda'],
                                        'imballoAziendaUnitaMisura': message['imballoAziendaUnita']



                                    })

@socketio.on( 'modifica_capitolato', namespace='/prezzarioProdotti')
def handle_modifica_capitolato(message):
    CapitolatoProdotto.registraCapitolato(nome=message['nome_prodotto'], modello=message['modello'],
                                           tipologia=message['tipologia'], marchio=message['marchio'])


@socketio.on('settaProdottoDaVerificare', namespace='/prezzarioProdotti')
def handle_settaProdottoDaVerificare(message):
    app.server.logger.info('ook\n\n\n')
    ModelloProdotto.setDaVerificare(tipologia=message['tipologia'], prodotto=message['prodotto'],
                                    marchio=message['marchio'], modello=message['modello'], valore=message['valore'])


@socketio.on('modifica_tipologia_prodotto', namespace='/prezzarioProdotti')
def handle_modifica_tipologia_prodotto(message):
    TipologiaProdotto.modificaTipologiaProdotto(nome=message['newNome'], oldNome=message['oldNome'])


@socketio.on('elimina_tipologia_prodotto', namespace='/prezzarioProdotti')
def handle_elimina_tipologia_prodotto(message):
    TipologiaProdotto.eliminaTipologiaProdotto(message['nome'])



@socketio.on('aggiungi_modello_prodotto', namespace='/prezzarioProdotti')
def handle_aggiungi_modello_prodotto(message):
    ModelloProdotto.registraModelloProdotto(nome=message['nome'], tipologia=message['tipologia'])

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    emit('aggiornaPagina', namespace='/prezzarioProdotti', room=dip.session_id)


@socketio.on('registra_nuovo_preventivo_nuova_commessa', namespace='/preventivoFiniture')
def handle_registra_nuovo_preventivo_nuova_commessa(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    idPreventivo = PreventivoFiniture.registraPreventivo_nuovaCommessa(nome_cliente=message['nome_cliente'],
                                       cognome_cliente=message['cognome_cliente'], indirizzo_cliente=message['indirizzo_cliente'],
                                        dipendente_generatore=dip.username,
                                        intervento_commessa=message['intervento'],
                                        indirizzo_commessa=message['indirizzo'],
                                        comune_commessa=message['comune'])

    app.preventivoFinitureSelezionato=idPreventivo
    emit('confermaRegistrazionePreventivo', namespace='/preventivoFiniture', room=dip.session_id)

@socketio.on('registra_nuovo_preventivo_vecchia_commessa', namespace='/preventivoFiniture')
def handle_registra_nuovo_preventivo_vecchia_commessa(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    idPreventivo = PreventivoFiniture.registraPreventivo_vecchiaCommessa(dipendente_generatore=dip.username, numero_preventivo=message['numero_preventivo'] )


    app.preventivoFinitureSelezionato=idPreventivo
    emit('confermaRegistrazionePreventivo', namespace='/preventivoFiniture', room=dip.session_id)

@socketio.on('modifica_preventivo_finiture', namespace='/preventivoFiniture')
def handle_modifica_preventivo_finiture(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    idPreventivo = PreventivoFiniture.modificaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'], dipendente_generatore=dip.username)
    app.preventivoFinitureSelezionato=idPreventivo

    emit('startModificaPreventivo', namespace='/preventivoFiniture', room=dip.session_id)


@socketio.on('add_nuovo_prodotto', namespace='/preventivoFiniture')
def handle_add_nuovo_prodotto(message):

    app.server.logger.info('\n\n\nMAAAAA\n\n\n')
    PreventivoFiniture.registraProdotto(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                        ordine=message['ordine'], tipologia=message['tipologia'], modello=message['modello'],
                                        marchio=message['marchio'], nome_prodotto=message['prodotto'], quantita=message['quantita'],
                                        unitaMisura=message['unitaMisura'], codice=message['codice'],
                                        diffCapitolato=message['diffCapitolato'])

@socketio.on('modifica_ordine_prodotto', namespace='/preventivoFiniture')
def handle_modifica_ordine_prodotto(message):
    PreventivoFiniture.iniziaRiordinoProdotti(numero_preventivo=message['numero_preventivo'], data=message['data'])

    PreventivoFiniture.modificaOrdineProdotto(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                              oldOrdine=message['ordineVecchio'], ordine=message['ordineNuovo'])

@socketio.on('modifica_prodotto', namespace='/preventivoFiniture')
def handle_modifica_prodotto(message):

    PreventivoFiniture.modificaProdotto(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                        ordine=message['ordine'], modifica={'quantita': message['quantita'],
                                                                            'diffCapitolato': message['diffCapitolato']})


@socketio.on('modifica_unita_misura', namespace='/preventivoFiniture')
def handle_modifica_prodotto(message):
    PreventivoFiniture.modificaProdotto(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                        ordine=message['ordine_prodotto'], modifica={'unitaMisura': message['value'] })

@socketio.on('modifica_nome_prodotto', namespace='/preventivoFiniture')
def handle_modifica_prodotto(message):
    PreventivoFiniture.modificaProdotto(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                        ordine=message['ordine_prodotto'], modifica={'nome_modificato': message['value'] })

@socketio.on('elimina_preventivo', namespace='/preventivoFiniture')
def handle_elimina_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoFiniture.eliminaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'])


    preventiviRestanti = PreventivoFiniture.get_counter_preventivi_per_numero(numero_preventivo=message['numero_preventivo'])


    emit('aggiornaAnteprimaPreventivoFiniture',
                    {
                        'numero_preventivo_deleted' : message['numero_preventivo'],
                        'data_deleted' : message['data'],
                        'preventivi_restanti': preventiviRestanti

                    }, namespace='/preventivoFiniture', room=dip.session_id)

@socketio.on('elimina_prodotto', namespace='/preventivoFiniture')
def handle_elimina_prodotto(message):

    PreventivoFiniture.eliminaProdotto(numero_preventivo=message['numero_preventivo'], data=message['data'], ordine=message['ordine'])

@socketio.on('stampa_preventivo', namespace='/preventivoFiniture')
def handle_stampa_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoFiniture.stampaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'], iva=message['iva'],
                                     tipoSconto=message['tipoSconto'], sconto=message['sconto'],
                                     chiudiPreventivo=message['chiudiPreventivo'], sumisura=message['sumisura'])

    emit('procediADownload', namespace='/preventivoFiniture', room=dip.session_id)

@socketio.on('inserisci_note', namespace='/preventivoFiniture')
def handle_inserisci_note(message):
    PreventivoFiniture.inserisciNote(numero_preventivo=message['numero_preventivo'], data=message['data'], nota=message['nota'])


@socketio.on('registra_nuovo_preventivo', namespace='/preventivoVarianti')
def handle_registra_nuovo_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    idPreventivo = PreventivoVarianti.registraPreventivo( dipendente_generatore=dip.username, numero_preventivo=message['numero_preventivo'] )

    app.preventivoVariantiSelezionato=idPreventivo
    emit('confermaRegistrazionePreventivo', namespace='/preventivoVarianti', room=dip.session_id)

@socketio.on('elimina_preventivo', namespace='/preventivoVarianti')
def handle_elimina_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoVarianti.eliminaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'])


    preventiviRestanti = PreventivoFiniture.get_counter_preventivi_per_numero(numero_preventivo=message['numero_preventivo'])


    emit('aggiornaAnteprimaPreventivoVarianti',
                    {
                        'numero_preventivo_deleted' : message['numero_preventivo'],
                        'data_deleted' : message['data'],
                        'preventivi_restanti': preventiviRestanti

                    }, namespace='/preventivoVarianti', room=dip.session_id)


@socketio.on('modifica_preventivo_varianti', namespace='/preventivoVarianti')
def handle_modifica_preventivo_varianti(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    idPreventivo = PreventivoVarianti.modificaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'], dipendente_generatore=dip.username)
    app.preventivoVariantiSelezionato=idPreventivo

    emit('startModificaPreventivo', namespace='/preventivoVarianti', room=dip.session_id)


@socketio.on('add_nuova_lavorazione', namespace='/preventivoVarianti')
def handle_add_nuova_lavorazione(message):

    PreventivoVarianti.registraLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                         ordine=message['ordine'], settore=message['settore'], tipologia_lavorazione=message['lavorazione'],
                                        numero=1, larghezza=1, altezza=1, profondita=1, unitaMisura=message['unitaMisura'],
                                        prezzoUnitario=message['prezzoUnitario'])

@socketio.on('elimina_lavorazione', namespace='/preventivoVarianti')
def handle_elimina_lavorazione(message):
    PreventivoVarianti.eliminaLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'], ordine=message['ordine'])

@socketio.on('modifica_ordine_lavorazione', namespace='/preventivoVarianti')
def handle_modifica_ordine_lavorazione(message):

    PreventivoVarianti.iniziaRiordinoLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'])

    PreventivoVarianti.modificaOrdineLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                            ordine=int('-'+message['ordineVecchio']), modifica={'ordine' : message['ordineNuovo']})

@socketio.on('add_nuova_sottolavorazione', namespace='/preventivoVarianti')
def handle_add_nuova_sottolavorazione(message):
    PreventivoVarianti.nuovaSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                           ordine=message['ordine'])

@socketio.on('elimina_sottolavorazione', namespace='/preventivoVarianti')
def handle_elimina_sottolavorazione(message):
    PreventivoVarianti.eliminaSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                             ordine=message['ordine'], ordine_sottolavorazione=message['ordine_sottolavorazione'])

@socketio.on('modifica_ordine_sottolavorazione', namespace='/preventivoVarianti')
def handle_modifica_ordine_sottolavorazione(message):


    PreventivoVarianti.iniziaRiordinoSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'], ordine=message['ordine'],
                                                   unitaMisura=message['unitaMisura'])

    PreventivoVarianti.modificaOrdineSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                                   ordine=message['ordine'],
                                                   old_ordine_sottolavorazione=int('-' + message['oldOrdineSottolav']),
                                                   new_ordine_sottolavorazione=message['newOrdineSottolav'],
                                                   unitaMisura=message['unitaMisura'])


@socketio.on('modifica_sottolavorazione', namespace='/preventivoVarianti')
def handle_modifica_sottolavorazione(message):

    message = json.loads(message)

    numero_preventivo = message.pop("numero_preventivo")
    data = message.pop("data")
    ordine = message.pop("ordine")
    ordine_sottolavorazione = message.pop("ordine_sottolavorazione")
    unitaMisura = message.pop("unitaMisura")

    PreventivoVarianti.modificaSottolavorazione(numero_preventivo=numero_preventivo, data=data,
                                                 ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione,
                                                 modifica=message, unitaMisura=unitaMisura)

@socketio.on('stampa_preventivo', namespace='/preventivoVarianti')
def handle_stampa_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoVarianti.stampaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'], iva=message['iva'],
                                     tipoSconto=message['tipoSconto'], sconto=message['sconto'],
                                     chiudiPreventivo=message['chiudiPreventivo'], sumisura=message['sumisura'])

    emit('procediADownload', namespace='/preventivoVarianti', room=dip.session_id)

@socketio.on('inserisci_note', namespace='/preventivoVarianti')
def handle_inserisci_note(message):
    PreventivoVarianti.inserisciNote(numero_preventivo=message['numero_preventivo'], data=message['data'], nota=message['nota'])


#################################################################################################################

@socketio.on('inserisci_note', namespace='/preventivoEdile')
def handle_inserisci_note(message):
    PreventivoEdile.inserisciNote(numero_preventivo=message['numero_preventivo'], data=message['data'], nota=message['nota'])


@socketio.on('modifica_ricarico_sottolav', namespace='/preventivoEdile')
def handle_modifica_ricarico_sottolav(message):

    PreventivoEdile.modificaSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                             ordine=message['ordine_lavorazione'], ordine_sottolavorazione=message['ordine_sottolav'],
                                             unitaMisura=message['unitaMisura'], modifica={'ricarico' : message['ricarico'], 'prezzoBase' : message['prezzoBase']});

@socketio.on('registra_nuovo_preventivo', namespace='/preventivoEdile')
def handle_registra_nuovo_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    idPreventivo = PreventivoEdile.registraPreventivo(nome_cliente=message['nome_cliente'],
                                       cognome_cliente=message['cognome_cliente'], indirizzo_cliente=message['indirizzo_cliente'],
                                        dipendente_generatore=dip.username,
                                          intervento_commessa=message['intervento_commessa'],
                                          indirizzo_commessa=message['indirizzo_commessa'],
                                          comune_commessa=message['comune_commessa'])

    app.preventivoEdileSelezionato=idPreventivo
    emit('confermaRegistrazionePreventivo', namespace='/preventivoEdile', room=dip.session_id)


@socketio.on('modifica_nome_lavorazione', namespace='/preventivoEdile')
def handle_modifica_prodotto(message):
    PreventivoEdile.modificaLavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                        ordine=message['ordine_lavorazione'], modifica={'nome_modificato': message['value'] })

@socketio.on('elimina_preventivo', namespace='/preventivoEdile')
def handle_elimina_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoEdile.eliminaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'])


    preventiviRestanti = PreventivoEdile.get_counter_preventivi_per_numero(numero_preventivo=message['numero_preventivo'])


    emit('aggiornaAnteprimaPreventivoEdile',
                    {
                        'numero_preventivo_deleted' : message['numero_preventivo'],
                        'data_deleted' : message['data'],
                        'preventivi_restanti': preventiviRestanti

                    }, namespace='/preventivoEdile', room=dip.session_id)

@socketio.on('modifica_preventivo_edile', namespace='/preventivoEdile')
def handle_modifica_preventivo_edile(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()


    idPreventivo = PreventivoEdile.modificaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'], dipendente_generatore=dip.username)
    app.preventivoEdileSelezionato=idPreventivo


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


    PreventivoEdile.iniziaRiordinoSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'], ordine=message['ordine'],
                                                   unitaMisura=message['unitaMisura'])

    PreventivoEdile.modificaOrdineSottolavorazione(numero_preventivo=message['numero_preventivo'], data=message['data'],
                                                   ordine=message['ordine'],
                                                   old_ordine_sottolavorazione=int('-' + message['oldOrdineSottolav']),
                                                   new_ordine_sottolavorazione=message['newOrdineSottolav'],
                                                   unitaMisura=message['unitaMisura'])


@socketio.on('modifica_sottolavorazione', namespace='/preventivoEdile')
def handle_modifica_sottolavorazione(message):

    #app.server.logger.info("\n\nEntrato in mod_sottolav: messaggio: {}\n\n".format(message))

    app.server.logger.info('mmm non capisco {}'.format(message['data']))

    numero_preventivo = message["numero_preventivo"]
    data = message["data"]
    ordine = message["ordine"]
    ordine_sottolavorazione = message["ordine_sottolavorazione"]
    unitaMisura = message["unitaMisura"]

    toChange = { message['fieldToChange'] : message['newValue']}

    PreventivoEdile.modificaSottolavorazione(numero_preventivo=numero_preventivo, data=data,
                                                 ordine=ordine, ordine_sottolavorazione=ordine_sottolavorazione,
                                                 modifica=toChange, unitaMisura=unitaMisura)


@socketio.on('stampa_preventivo', namespace='/preventivoEdile')
def handle_stampa_preventivo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    PreventivoEdile.stampaPreventivo(numero_preventivo=message['numero_preventivo'], data=message['data'], iva=message['iva'],
                                     tipoSconto=message['tipoSconto'], sconto=message['sconto'],
                                     chiudiPreventivo=message['chiudiPreventivo'], sumisura=message['sumisura'])

    emit('procediADownload', namespace='/preventivoEdile', room=dip.session_id)


@socketio.on('imposta appuntamento', namespace='/agenda')
def handle_imposta_appuntamento(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()


    returnVal =Agenda.registraAppuntamento(dipendente=dip.username, titolo=message['titolo'], giorno=message['giorno'],
                          inizio_ora=message['inizio_ora'], fine_ora=message['fine_ora'])

    emit('responso_imposta_appuntamento', {'risposta': returnVal, 'giorno': message['giorno'], 'titolo': message['titolo'],
                                           'inizioH': message['inizio_ora'],'fineH': message['fine_ora']}, namespace='/agenda', room=dip.session_id )


@socketio.on('cambia_orario_inizio', namespace='/agenda')
def handle_cambia_orario_inizio(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()
    old_start=message['old_inizio'].split(':')[0]+':'+message['old_inizio'].split(':')[1]
    app.server.logger.info('\n\n\n1n1n1nJJJJqqua entrp! {} \n {} \n\n\n'.format( old_start, message['new_inizio']))

    retVal = Agenda.cambiaOrarioInizioEvento(dipendente=message['dip'], giorno=message['giorno'],
                                             old_inizio_ora=old_start, new_inizio_ora=message['new_inizio'])

    emit('responso_modifica_inizioOra', {'risposta': retVal}, namespace='/agenda', room=dip.session_id )

@socketio.on('cambia_orario_fine', namespace='/agenda')
def handle_cambia_orario_fine(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    retVal = Agenda.cambiaOrarioInizioEvento(dipendente=message['dip'], giorno=message['giorno'],
                                             old_fine_ora=message['old_fine'], new_fine_ora=message['new_fine'])

    emit('responso_modifica_inizioOra', namespace='/agenda', room=dip.session_id)

@socketio.on('elimina_appuntamento', namespace='/agenda')
def handle_elimina_appuntamento(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    Agenda.eliminaAppuntamento(dipendente=message['dip'], giorno=message['giorno'], inizio_ora=message['inizio_ora'])

    emit('responso_elimina_appuntamento', namespace='/agenda', room=dip.session_id)


'''
@socketio.on('imposta_sopraluogo', namespace='/agenda')
def handle_imposta_sopraluogo(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    app.server.logger.info('\n\nStampo la data {} e intervallo {} \n\n'.format(message['giorno'], message['ora']))
    titolo = "Sopraluogo cliente {}".format(message['cliente'])
    Agenda.registraEvento(dipendente=dip.username, titolo=titolo, start_date=message['giorno'],
                          durata_giorni=1, tipologia=False,
                          start_hour=message['ora'], durata_ore=message['durata'],
                          accompagnatore_sopraluogo=message['accompagnatore'], cliente_sopraluogo=message['cliente'],
                          sopraluogo=True, luogo_sopraluogo=message['luogo'])
'''
@socketio.on('modifica_profilo', namespace='/profilo')
def handle_modifica_profilo(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    if message['campo'] == 'nome_cognome':
        nome = message['valore'].split(' ')[0]
        cognome = message['valore'].split(' ')[1]
        Dipendente.modificaProfilo(username=dip.username, modifica={'nome': nome, 'cognome': cognome})

    else:
        Dipendente.modificaProfilo(username=dip.username, modifica={message['campo'] : message['valore']})

    emit('aggiorna_pagina', namespace='/profilo', room=dip.session_id)

@socketio.on('modifica_indirizzo_profilo', namespace='/profilo')
def handle_modifica_profilo(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    if message['campo'] == 'residenza':
        Dipendente.modificaProfilo(username=dip.username, modifica={'residenzaVia': message['via'], 'residenzaNum': message['num'], 'residenzaCitta': message['citta'], 'residenzaRegione': message['regione']})
    else:
        Dipendente.modificaProfilo(username=dip.username, modifica={'domicilioVia': message['via'], 'domicilioNum': message['num'], 'domicilioCitta': message['citta'], 'domicilioRegione': message['regione']})

    emit('aggiorna_pagina', namespace='/profilo', room=dip.session_id)

@socketio.on('aggiungi_ferie', namespace='/profilo')
def handle_aggiungi_ferie(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    Calendario.registraEvento(dipendente=dip.username, titolo=message['titolo'],
                              start_date=message['start_date'], end_date=message['end_date'],
                              luogo="", tipologia=False)


@socketio.on('richiesta_ferie', namespace='/profilo')
def handle_richiesta_ferie(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()
    dirigenti = Dirigente.query.all()

    RichiestaFerie.registraRichiesta(dipendente=dip.username, titolo=message['titolo'], start_date=message['start_date'],
                                     end_date=message['end_date'])

    for dirigente in dirigenti:
        dipDirigente = Dipendente.query.filter_by(username=dirigente.username).first()

        num=Notifica.registraNotifica(destinatario=dipDirigente.username, titolo="Richiesta ferie di {0} {1}".format(dip.nome, dip.cognome),
                                  contenuto="{} {} ha richiesto delle ferie dal {} al {}".format(dip.nome, dip.cognome,
                                                                                                  message['start_date'], message['end_date']),
                                  tipologia='richiestaFerie', richiedente_ferie=dip.username, start_date=message['start_date'])

        emit('aggiornaNotifiche', {'titolo': "Richiesta ferie di {0} {1}".format(dip.nome, dip.cognome),
                                   'contenuto': "{} {} ha richiesto delle ferie dal {} al {}.".format(dip.nome, dip.cognome,
                                                                                                  message['start_date'], message['end_date']),
                                   'tipologia' : "richiestaFerie", 'numero': num},
                                    namespace='/notifica', room=dipDirigente.session_id)

@socketio.on('elimina_ferie', namespace='/profilo')
def handle_aggiungi_ferie(message):


    dip = Dipendente.query.filter_by(username=message['dip']).first()

    Calendario.eliminaEvento(dipendente=dip.username, titolo=message['titolo'],
                              start_date=message['start_date'], tipologia=False)

    emit('aggiorna_pagina', namespace='/profilo', room=dip.session_id)

@socketio.on('modifica_ferie', namespace='/profilo')
def handle_modifica_ferie(message):


    dip = Dipendente.query.filter_by(username=message['dip']).first()

    Calendario.modificaFerie(dipendente=dip.username, oldTitolo=message['oldTitolo'],
                             newTitolo=message['newTitolo'], start_date=message['start_date'])

    emit('aggiorna_pagina', namespace='/profilo', room=dip.session_id)

@socketio.on('imposta_evento_calendario', namespace='/calendario')
def handle_imposta_evento_calendario(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()

    Calendario.registraEvento(dipendente=dip.username, titolo=message['titolo'],
                              start_date=message['start_date'], end_date=message['end_date'],
                              tipologia=True, descrizione=message['descrizione'])

    emit('conferma_registrazione_evento', namespace='/calendario', room=dip.session_id)

@socketio.on('elimina_evento_calendario', namespace='/calendario')
def handle_elimina_evento_calendario(message):

    dip = Dipendente.query.filter_by(username=message['dip']).first()


    Calendario.eliminaEvento(dipendente=message['dipendente_generatore'], titolo=message['titolo'],
                              start_date=message['start_date'], tipologia=True )

    emit('conferma_eliminazione_evento', namespace='/calendario', room=dip.session_id)


@socketio.on('chat_message', namespace='/chat')
def handle_chat_message(message):

    mittente = Dipendente.query.filter_by(username=message['mittente']).first()
    destinatario = Dipendente.query.filter_by(username=message['destinatario']).first()

    ( timestamp, msgForDestHtml ) = Messaggio.registraMessaggio(mittente=message['mittente'], destinatario=message['destinatario'], testo=message['testo'])

    data="{}/{}/{}".format(timestamp[0].day,timestamp[0].month,timestamp[0].year)
    ora="{}:{}:{}".format(timestamp[1].hour,timestamp[1].minute,timestamp[1].second)


    emit("impostaTimestamp", {'data': data, 'ora': ora}, namespace='/chat', room=mittente.session_id)

    emit("nuovoMessaggio", {'htmlMsg': msgForDestHtml, 'mittente': mittente.username}, namespace='/chat', room=destinatario.session_id)

@socketio.on('storico_messaggi', namespace='/chat')
def handle_storico_messaggi(message):
    mittente = Dipendente.query.filter_by(username=message['mittente']).first()
    htmlChat = Messaggio.recuperaConversazioni(mittente=message['mittente'], destinatario=message['destinatario'])

    emit("stampaStorico", {'htmlChat': htmlChat}, namespace='/chat', room=mittente.session_id)

@socketio.on('cerca_colleghi_msg_non_letti', namespace="/chat")
def handle_cerca_colleghi_msg_non_letti(message):
    dip = Dipendente.query.filter_by(username=message['dip']).first()

    colleghi = Messaggio.returnColleghiMessaggiNonLetti(destinatario=dip.username)

    for collega in colleghi:
        emit('blinka_collega', {'collega': collega}, namespace='/chat', room=dip.session_id)


@socketio.on('messaggio_letto', namespace="/chat")
def handle_messaggio_letto(message):
    Messaggio.messaggioLetto(mittente=message['mittente'], destinatario=message['destinatario'])

@socketio.on('cambia_livello_difficolta', namespace="/cliente")
def handle_cambia_livello_difficolta(message):

    ClienteAccolto.modificaDifficolta(nome=message['nome'], cognome=message['cognome'],
                                      indirizzo=message['indirizzo'], valore=message['valore'])


@socketio.on_error('/cliente')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))


@socketio.on_error('/chat')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/calendario')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))


@socketio.on_error('/profilo')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))


@socketio.on_error('/agenda')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/impegni')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))


@socketio.on_error('/home')
def error_handler(e):
    server.logger.info("\n\n\nci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/notifica')
def error_handler_notifica(e):
    server.logger.info("\n\n\nnotifica: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/prezzario')
def error_handler(e):
    server.logger.info("\n\n\nprezzario edile: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/artigiani')
def error_handler(e):
    server.logger.info("\n\n\nartigiani: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/fornitore')
def error_handler(e):
    server.logger.info("\n\n\nfornitore: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/prezzarioProdotti')
def error_handler(e):
    server.logger.info("\n\n\nprezzario prodotti: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/preventivoEdile')
def error_handler(e):
    server.logger.info("\n\n\npreventivo edile: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/preventivoFiniture')
def error_handler(e):
    server.logger.info("\n\n\npreventivo finiture: ci sono probelmi {}\n\n\n".format(e))

@socketio.on_error('/preventivoVarianti')
def error_handler(e):
    server.logger.info("\n\n\npreventivo varianti: ci sono probelmi {}\n\n\n".format(e))