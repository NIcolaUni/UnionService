from flask import Flask, render_template, redirect
from app import server, database
from app.model.form import DipFittizioForm, LoginForm, CompletaProfilo
from app.model.dipendenteFittizio import DipendenteFittizio
from app.model.db.dipRegistratoDBmodel import DipRegistratoDBmodel
from app.model.dipendente import Dipendente
from flask_login import current_user, login_user

@server.route('/homeheader')
def homeheader():
    return render_template('header_homepage.html')

@server.route('/gestioneDip', methods=['GET','POST'])
def gestioneDip():
    form = DipFittizioForm()
    if form.validate_on_submit():
        dipReg = DipRegistratoDBmodel(username=form.username.data, password=form.password.data, fittizio=True)
        newDipFittizio = DipendenteFittizio(username=form.username.data, password=form.password.data, classe=form.tipo_dip.data, dirigente=form.dirigente.data)
        database.session.add(dipReg)
        database.session.add(newDipFittizio)
        database.session.commit()
        return redirect('/homepage')
    else:
        form.assegnaUserEPass()
        return render_template('gestioneDip.html', form=form )

@server.route('/paginaProfilo')
def paginaProfilo():
    return render_template('paginaProfilo.html')

@server.route('/homepage')
def index():
    return render_template('homepage.html')

@server.route('/registraDipendente', methods=['GET','POST'])
def registraDipendente():
    form = CompletaProfilo()
    return render_template("registrazioneDip.html", form=form)


@server.route('/', methods=['GET','POST'])
@server.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return render_template("homepage.html")

    form = LoginForm()

    if form.validate_on_submit():
        dip=DipRegistratoDBmodel.query.filter_by(username=form.username.data, password=form.password.data).first()
        if dip is None:
            return render_template("login.html", form=form, error="Credenziali errate!")

       # print("\n\n\n\n\nBELLA IO SONO IL DIP {0}{1}".format(dip.username, dip.fittizio))

        if dip.fittizio :
            dip=DipendenteFittizio.query.filter_by(username=dip.username).first()
            login_user(dip)
            return redirect('/registraDipendente')
        return render_template("homepage.html")


    return render_template("login.html", form=form)

if __name__ == '__main__':
    	app.run(host='0.0.0.0', port=8000)
