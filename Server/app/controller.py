from flask import Flask, render_template, redirect, request, url_for
from app import server, database
from app.model.form import DipFittizioForm, LoginForm, RegistraDipendenteForm
from app.model.dipendenteFittizio import DipendenteFittizio
from app.model.dipendenteRegistrato import DipendenteRegistrato
from app.model.dipendente import Dipendente
from flask_login import current_user, login_user, login_required

@server.route('/homeheader')
@login_required
def homeheader():
    return render_template('header_homepage.html')

@server.route('/gestioneDip', methods=['GET','POST'])
@login_required
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():
        dipReg = DipendenteRegistrato(username=form.username.data, password=form.password.data, fittizio=True)
        newDipFittizio = DipendenteFittizio(username=form.username.data, password=form.password.data, classe=form.tipo_dip.data, dirigente=form.dirigente.data)
        database.session.add(dipReg)
        database.session.add(newDipFittizio)
        database.session.commit()
        return redirect('/homepage')
    else:
        form.assegnaUserEPass()
        return render_template('gestioneDip.html', form=form )

@server.route('/paginaProfilo')
@login_required
def paginaProfilo():
    return render_template('paginaProfilo.html')


@server.route('/homepage')
@login_required
def homepage():
    dip=Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('homepage.html', dipendente=dip)

@server.route('/sidebarLeft')
@login_required
def sidebarLeft():
    dip = Dipendente.query.filter_by(username=current_user.get_id()).first()
    return render_template('sidebar-left.html', dipendente=dip)

@server.route('/header')
@login_required
def header():
    return render_template('header.html')

@server.route('/registraDipendente', methods=['GET','POST'])
@login_required
def registraDipendente():
    form = RegistraDipendenteForm()

    if form.validate_on_submit():

        dipFittizio=DipendenteFittizio.query.filter_by(username=current_user.get_id()).first();
        username_candidato = "{0}_{1}".format(form.nome.data, form.cognome.data).lower()

        counter = 0
        if DipendenteRegistrato.query.filter_by(username=username_candidato).first() != None:
            counter = 1
            while DipendenteRegistrato.query.filter_by(username="{0}{1}".format(username_candidato, counter)).first() != None:
             counter += 1

        dip = None

        if counter == 0:
            dip = DipendenteRegistrato(username=username_candidato, password=form.password.data, fittizio=False)
        else:
            dip = DipendenteRegistrato(username="{0}{1}".format(username_candidato, counter), password=form.password.data, fittizio=False)



        newDip = Dipendente(nome=form.nome.data, cognome=form.cognome.data, cf=form.cf.data,
                                dataNascita=form.dataNascita.data, sesso=form.sesso.data,
                                via=form.via.data, civico=form.civico.data, cap=form.cap.data,
                                citta=form.citta.data, regione=form.regione.data, telefono=form.telefono.data,
                                username=dip.username, password=dip.password, email_aziendale=form.email_aziendale.data,
                                email_personale=form.email_personale.data, iban=form.iban.data, partitaIva=form.partitaIva.data,
                                classe=dipFittizio.classe, dirigente=dipFittizio.dirigente)
        database.session.delete(dipFittizio)
        database.session.delete(DipendenteRegistrato.query.filter_by(username=current_user.get_id()).first())
        database.session.add(dip)
        database.session.add(newDip)
        database.session.commit()
        return redirect('/')


    return render_template("registrazioneDip.html", form=form)


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

if __name__ == '__main__':
    	app.run(host='0.0.0.0', port=8000)
